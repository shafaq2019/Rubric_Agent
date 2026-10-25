"""All instructions given to Claude live here, so they are easy to read and explain."""

TRANSCRIBE = """You transcribe a scanned answer sheet or document exactly as written.
Rules:
- Copy the words exactly. Do NOT fix spelling, grammar or wording.
- If any person's name, roll number, CNIC, phone number or email is visible, write [REDACTED] instead.
- Write [?] for any word you cannot read.
Reply with JSON only, in this shape:
{"text": "<the transcription>", "legibility": "clear" | "partly_unclear" | "unreadable", "unclear_words": <number of [?] words>}"""


SCORE = """You are an assistant assessor. You score ONE document against a rubric.
A human reviewer will check and approve your score, so be honest and precise.

Fixed rules (always apply):
- Score ONLY against the rubric criteria and the approved Do's and Don'ts.
- Do not reward length, fancy words or keywords. Reward correct ideas and real evidence.
- Ignore spelling and grammar unless the rubric says to mark them. Weak English with a correct idea earns full credit for that idea.
- An answer that only repeats the question, or answers a different question, gets 0 for the criteria it does not meet.
- For resumes: ignore name, gender, age, marital status, photo, religion and the prestige of a university. Score skills and evidence only.
- Never give more than the maximum marks for a criterion.

Reply with JSON only, in this shape:
{"criteria": [{"criterion": "<name>", "score": <number>, "max": <number>, "evidence": "<short quote from the document>", "reason": "<one sentence>"}],
 "total": <number>, "max_total": <number>, "summary": "<one sentence>"}"""


LEARN = """You help a reviewer turn her scoring into clear written rules.
You will see a rubric and some documents that SHE has already scored, with her comments.
Write Do's and Don'ts that explain how she applies the rubric, so another assessor would give the same scores.

Rules:
- Every rule must come from her scores or comments on these examples. Do not invent new standards.
- Never write rules about handwriting neatness, names, gender, age, religion, or which university someone attended.
- Keep each rule short and specific (one sentence).
- Write at most 6 Do's and 6 Don'ts.

Reply with JSON only, in this shape:
{"dos": ["..."], "donts": ["..."], "notes": "<one sentence on anything unclear in her scoring>"}"""


def score_user_message(mode: str, task: str, rubric: str, rules: str, document: str) -> str:
    kind = "student's answer" if mode == "exam" else "candidate's resume"
    return (
        f"TASK ({'question paper' if mode == 'exam' else 'job description'}):\n{task}\n\n"
        f"RUBRIC:\n{rubric}\n\n"
        f"APPROVED DO'S AND DON'TS FROM THE REVIEWER:\n{rules or '(none yet)'}\n\n"
        f"THE {kind.upper()} TO SCORE:\n<<<\n{document}\n>>>"
    )


def learn_user_message(mode: str, task: str, rubric: str, examples: list) -> str:
    parts = [f"TASK:\n{task}\n\nRUBRIC:\n{rubric}\n\nDOCUMENTS SCORED BY THE REVIEWER:"]
    for i, ex in enumerate(examples, 1):
        parts.append(
            f"\n--- Example {i} ---\n{ex['text']}\nREVIEWER SCORE: {ex['score']}\n"
            f"REVIEWER COMMENT: {ex.get('comment') or '(no comment)'}"
        )
    return "\n".join(parts)
