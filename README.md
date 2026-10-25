# Rubric-Based Assessment Agent (DATA722 mid-term)

One agent that scores documents against a rubric after learning from a human reviewer.
Two scopes: **exam grading** (typed or scanned handwritten answers) and **resume screening**.

**Flow:** reviewer scores a random 15% sample → agent drafts Do's & Don'ts from her scoring and
tests itself on held-out samples → reviewer approves the rules → agent scores the rest (3 runs each,
unstable or hard-to-read items are flagged) → reviewer approves every score.

All demo data is synthetic. Personal details are removed before anything is sent to Claude.

## Files
| File | What it does |
|---|---|
| `api/index.py` | Backend (FastAPI): the routes the web page calls |
| `core/agent.py` | The agent: transcribe, score 3 times, flag, learn rules, self-test |
| `core/prompts.py` | Every instruction sent to Claude |
| `core/llm.py` | Calls Claude and counts tokens and cost |
| `core/redact.py` | Removes names, CNIC, phone, email, age, gender, etc. |
| `core/page.py` | Frontend (HTML + JavaScript) |
| `core/demo_data.py` | Small synthetic demo sets |
| `requirements.txt` | Library list |
| `vercel.json` | Tells Vercel how to run the app |

## Settings (Vercel → Project → Settings → Environment Variables)
- `ANTHROPIC_API_KEY` (required)
- `CLAUDE_MODEL` (optional, default `claude-sonnet-5-5`)
- `PRICE_IN_PER_MTOK`, `PRICE_OUT_PER_MTOK` (optional, USD per million tokens, for the cost display)

## Run on your own computer (optional)
```
python -m venv .venv
.venv\Scripts\activate        (Mac: source .venv/bin/activate)
pip install -r requirements.txt
set ANTHROPIC_API_KEY=your-key   (Mac: export ANTHROPIC_API_KEY=your-key)
uvicorn api.index:app --reload
```
Then open http://127.0.0.1:8000
