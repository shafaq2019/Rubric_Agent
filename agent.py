"""The agent: the decisions it makes for each document, and how it learns from the reviewer.

Loop for one batch:
  1. Reviewer scores a random 15% sample herself.
  2. learn_rules(): the agent drafts Do's & Don'ts from her scoring, tests itself on
     part of the sample it did NOT learn from, and decides: continue, or ask for more examples.
  3. Reviewer edits/approves the rules.
  4. score_document() on each remaining document: 3 runs -> stable? -> route to normal or full review.
  5. Reviewer approves every final score (in the UI).
"""
import asyncio
import random
import statistics

from core import prompts
from core.llm import ask, parse_json, add_usage

RUNS = 3                 # each document is scored 3 times to measure stability
MIN_AGREEMENT = 0.70     # self-test bar: share of held-out samples within tolerance


def tolerance(max_total: float) -> float:
    """How far apart two scores can be and still 'agree': 1 mark, or 10% of the total if larger."""
    return max(1.0, 0.1 * (max_total or 0))


# ---------- reading scans ----------
async def transcribe(image_b64: str, media_type: str) -> dict:
    content = [
        {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": image_b64}},
        {"type": "text", "text": "Transcribe this document."},
    ]
    text, usage = await ask(prompts.TRANSCRIBE, content, max_tokens=2000)
    data = parse_json(text)
    legibility = data.get("legibility", "clear")
    # Agent decision: unreadable sheets are NOT scored; they go straight to the reviewer.
    route = "send_to_reviewer" if legibility == "unreadable" else "proceed"
    return {"text": data.get("text", ""), "legibility": legibility,
            "unclear_words": data.get("unclear_words", 0), "route": route, "usage": usage}


# ---------- scoring ----------
async def score_once(mode, task, rubric, rules, document) -> tuple[dict, dict]:
    msg = prompts.score_user_message(mode, task, rubric, rules, document)
    text, usage = await ask(prompts.SCORE, msg, max_tokens=1500)
    return parse_json(text), usage


async def score_document(mode, task, rubric, rules, document, legibility="clear") -> dict:
    """Scores one document RUNS times in parallel, then decides how to route it."""
    results = await asyncio.gather(*[score_once(mode, task, rubric, rules, document) for _ in range(RUNS)])
    usage = {}
    runs = []
    for data, u in results:
        add_usage(usage, u)
        runs.append(data)
    totals = [float(r.get("total", 0)) for r in runs]
    max_total = float(runs[0].get("max_total", 0) or 0)
    suggested = statistics.median(totals)
    spread = max(totals) - min(totals)
    # use the run closest to the median as the explanation shown to the reviewer
    best = min(runs, key=lambda r: abs(float(r.get("total", 0)) - suggested))

    flags = []
    if spread > tolerance(max_total):
        flags.append(f"Unstable: the 3 runs gave {', '.join(f'{t:g}' for t in totals)}")
    if legibility == "partly_unclear":
        flags.append("Some handwriting was unclear - check the transcription")
    route = "full_review" if flags else "normal_review"
    return {"suggested": suggested, "runs": totals, "max_total": max_total, "spread": spread,
            "criteria": best.get("criteria", []), "summary": best.get("summary", ""),
            "flags": flags, "route": route, "usage": usage}


# ---------- learning from the reviewer ----------
def _rules_text(data: dict) -> str:
    dos = "\n".join(f"DO: {d}" for d in data.get("dos", []))
    donts = "\n".join(f"DON'T: {d}" for d in data.get("donts", []))
    return (dos + "\n" + donts).strip()


async def _draft_rules(mode, task, rubric, examples) -> tuple[dict, dict]:
    text, usage = await ask(prompts.LEARN, prompts.learn_user_message(mode, task, rubric, examples), max_tokens=1200)
    return parse_json(text), usage


async def learn_rules(mode, task, rubric, examples, seed: int = 7) -> dict:
    """examples: [{"id", "text", "score", "comment"}] scored by the reviewer.

    Self-test: learn from about 2/3 of the examples, score the held-out 1/3 with those rules,
    and compare with the reviewer. Then learn the final rules from ALL examples.
    """
    usage = {}
    self_test = None
    if len(examples) >= 3:
        shuffled = examples[:]
        random.Random(seed).shuffle(shuffled)
        n_hold = max(1, len(shuffled) // 3)
        held, train = shuffled[:n_hold], shuffled[n_hold:]
        draft, u = await _draft_rules(mode, task, rubric, train)
        add_usage(usage, u)
        draft_rules = _rules_text(draft)
        scored = await asyncio.gather(*[score_once(mode, task, rubric, draft_rules, ex["text"]) for ex in held])
        rows = []
        for ex, (data, u2) in zip(held, scored):
            add_usage(usage, u2)
            ai = float(data.get("total", 0))
            tol = tolerance(float(data.get("max_total", 0) or 0))
            rows.append({"id": ex.get("id"), "reviewer": float(ex["score"]), "agent": ai,
                         "agree": abs(ai - float(ex["score"])) <= tol})
        agreement = sum(r["agree"] for r in rows) / len(rows)
        self_test = {"held_out": rows, "agreement": agreement}

    final, u = await _draft_rules(mode, task, rubric, examples)
    add_usage(usage, u)

    # Agent decision: continue, or ask for more reviewer examples first.
    if self_test is None:
        decision = "need_more_examples"
        message = "Fewer than 3 reviewer-scored examples, so I cannot test myself. Please score at least 3."
    elif self_test["agreement"] < MIN_AGREEMENT:
        decision = "need_more_examples"
        message = (f"On examples I did not learn from, I agreed with you on only {self_test['agreement']:.0%}. "
                   "Please score a few more documents before I continue.")
    else:
        decision = "ready"
        message = (f"On examples I did not learn from, I agreed with you on {self_test['agreement']:.0%}. "
                   "Please check the rules below, edit them, and approve.")
    return {"rules": _rules_text(final), "dos": final.get("dos", []), "donts": final.get("donts", []),
            "notes": final.get("notes", ""), "self_test": self_test, "decision": decision,
            "message": message, "usage": usage}
