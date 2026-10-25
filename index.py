"""FastAPI backend. Vercel runs this file. Each route below is one thing the web page can ask for."""
import io
import os
import sys

# make the project folder importable (so `core` can be found on Vercel and locally)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from core import agent, demo_data
from core.llm import MODEL, MOCK, cost_usd
from core.page import PAGE
from core.redact import redact

app = FastAPI(title="Rubric-Based Assessment Agent")


@app.exception_handler(Exception)
async def show_errors(request, exc):
    # send a readable error to the page instead of a blank failure
    return JSONResponse(status_code=500, content={"error": f"{type(exc).__name__}: {exc}"})


def with_cost(result: dict) -> dict:
    result["cost_usd"] = cost_usd(result.get("usage", {}))
    return result


# ---------- pages ----------
@app.get("/", response_class=HTMLResponse)
def home():
    return PAGE


@app.get("/api/health")
def health():
    return {"model": MODEL, "key_set": bool(os.getenv("ANTHROPIC_API_KEY")) or MOCK, "mock": MOCK}


@app.get("/api/demo/{mode}")
def demo(mode: str):
    data = demo_data.EXAM if mode == "exam" else demo_data.RESUME
    docs = []
    for d in data["documents"]:
        clean, n = redact(d["text"])
        docs.append({"id": d["id"], "label": d["label"], "text": clean, "redacted": n, "source": "typed"})
    return {"task": data["task"], "rubric": data["rubric"], "documents": docs}


# ---------- documents in ----------
class TextIn(BaseModel):
    text: str


@app.post("/api/redact")
def redact_text(body: TextIn):
    clean, n = redact(body.text)
    return {"text": clean, "redacted": n}


class ImageIn(BaseModel):
    image_b64: str
    media_type: str = "image/jpeg"


@app.post("/api/transcribe")
async def transcribe(body: ImageIn):
    result = await agent.transcribe(body.image_b64, body.media_type)
    clean, n = redact(result["text"])  # second safety net after the model's own redaction
    result["text"], result["redacted"] = clean, n
    return with_cost(result)


@app.post("/api/extract")
async def extract(file: UploadFile = File(...)):
    raw = await file.read()
    name = (file.filename or "").lower()
    if name.endswith(".pdf"):
        from pypdf import PdfReader
        text = "\n".join((p.extract_text() or "") for p in PdfReader(io.BytesIO(raw)).pages)
    elif name.endswith(".txt"):
        text = raw.decode("utf-8", errors="ignore")
    else:
        raise HTTPException(400, "Please upload a .pdf or .txt file (or an image for scanned sheets).")
    clean, n = redact(text)
    return {"text": clean.strip(), "redacted": n}


# ---------- agent steps ----------
class Example(BaseModel):
    id: str
    text: str
    score: float
    comment: str = ""


class LearnIn(BaseModel):
    mode: str
    task: str
    rubric: str
    examples: list[Example]


@app.post("/api/learn")
async def learn(body: LearnIn):
    examples = [{**e.model_dump(), "text": redact(e.text)[0]} for e in body.examples]
    return with_cost(await agent.learn_rules(body.mode, body.task, body.rubric, examples))


class ScoreIn(BaseModel):
    mode: str
    task: str
    rubric: str
    rules: str = ""
    text: str
    legibility: str = "clear"


@app.post("/api/score")
async def score(body: ScoreIn):
    text = redact(body.text)[0]
    return with_cost(await agent.score_document(body.mode, body.task, body.rubric, body.rules, text, body.legibility))
