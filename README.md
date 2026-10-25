# Rubric-Based Assessment Agent (DATA722 mid-term)

One agent that scores documents against a rubric after learning from a human reviewer.
Two scopes: **exam grading** (typed or scanned handwritten answers) and **resume screening**.

**Flow:** reviewer scores a random 15% sample → agent drafts Do's & Don'ts from her scoring and
tests itself on held-out samples → reviewer approves the rules → agent scores the rest (3 runs each,
unstable or hard-to-read items are flagged) → reviewer approves every score.

All demo data is synthetic. Personal details are removed before anything is sent to the AI model.
AI model: Google Gemini (free tier) by default; Claude also supported.

## Files
| File | What it does |
|---|---|
| `index.py` | Backend (FastAPI): the routes the web page calls |
| `agent.py` | The agent: transcribe, score 3 times, flag, learn rules, self-test |
| `prompts.py` | Every instruction sent to the AI model |
| `llm.py` | Calls the AI model (Gemini or Claude) and counts tokens and cost |
| `redact.py` | Removes names, CNIC, phone, email, age, gender, etc. |
| `page.py` | Frontend (HTML + JavaScript) |
| `demo_data.py` | Small synthetic demo sets |
| `requirements.txt` | Library list |
| `vercel.json` | Tells Vercel how to run the app |

## Settings (Vercel → Project → Settings → Environment Variables)
- `GEMINI_API_KEY` (required, free from aistudio.google.com)
- `GEMINI_MODEL` (optional, default `gemini-flash-lite-latest`)
- `RUNS` (optional, default 3 scoring runs per document)
- To use Claude instead: `PROVIDER=anthropic`, `ANTHROPIC_API_KEY`, `CLAUDE_MODEL`
- `PRICE_IN_PER_MTOK`, `PRICE_OUT_PER_MTOK` (optional, USD per million tokens, for the cost display)

## Run on your own computer (optional)
```
python -m venv .venv
.venv\Scripts\activate        (Mac: source .venv/bin/activate)
pip install -r requirements.txt
set GEMINI_API_KEY=your-key   (Mac: export GEMINI_API_KEY=your-key)
uvicorn index:app --reload
```
Then open http://127.0.0.1:8000
