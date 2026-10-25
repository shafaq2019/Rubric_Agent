"""Talks to the AI model. Every call returns (text, usage) so we can count tokens and cost.

Default: Google Gemini free tier (needs GEMINI_API_KEY, free from aistudio.google.com).
Optional: Claude (set PROVIDER=anthropic and ANTHROPIC_API_KEY).
"""
import asyncio
import json
import os
import re

import httpx

PROVIDER = os.getenv("PROVIDER", "anthropic" if os.getenv("ANTHROPIC_API_KEY") and not os.getenv("GEMINI_API_KEY") else "gemini")
if PROVIDER == "gemini":
    MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-lite-latest")
else:
    MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5")

# Price per million tokens (USD), used only for the cost display.
# Gemini free tier costs $0; the paid-tier price is shown so you can report what a real rollout would cost.
PRICE_IN = float(os.getenv("PRICE_IN_PER_MTOK", "0.10" if PROVIDER == "gemini" else "3"))
PRICE_OUT = float(os.getenv("PRICE_OUT_PER_MTOK", "0.40" if PROVIDER == "gemini" else "15"))
MOCK = os.getenv("MOCK_LLM") == "1"  # used only for offline testing

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def key_set() -> bool:
    return MOCK or bool(os.getenv("GEMINI_API_KEY" if PROVIDER == "gemini" else "ANTHROPIC_API_KEY"))


async def ask(system: str, content, max_tokens: int = 1500):
    """Send one message. `content` is a string, or a list of blocks:
    {"type": "text", "text": ...} or {"type": "image", "source": {"media_type": ..., "data": <base64>}}"""
    if MOCK:
        import mock
        return mock.reply(system, content)
    if PROVIDER == "gemini":
        return await _ask_gemini(system, content, max_tokens)
    return await _ask_claude(system, content, max_tokens)


async def _ask_gemini(system, content, max_tokens):
    blocks = [{"type": "text", "text": content}] if isinstance(content, str) else content
    parts = []
    for b in blocks:
        if b["type"] == "text":
            parts.append({"text": b["text"]})
        elif b["type"] == "image":
            parts.append({"inline_data": {"mime_type": b["source"]["media_type"], "data": b["source"]["data"]}})
    body = {
        "system_instruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {"maxOutputTokens": max_tokens, "responseMimeType": "application/json"},
    }
    url = GEMINI_URL.format(model=MODEL)
    headers = {"x-goog-api-key": os.getenv("GEMINI_API_KEY", "")}
    async with httpx.AsyncClient(timeout=50) as client:
        for attempt in range(3):
            r = await client.post(url, json=body, headers=headers)
            if r.status_code == 429 and attempt < 2:   # free-tier rate limit: wait and retry
                await asyncio.sleep(8 * (attempt + 1))
                continue
            break
        if r.status_code == 404:
            raise RuntimeError(f"Model '{MODEL}' not found. Set GEMINI_MODEL in Vercel to a model listed in "
                               "Google AI Studio (e.g. a Flash-Lite model).")
        if r.status_code == 429:
            raise RuntimeError("Gemini free-tier limit reached. Wait a minute (or until tomorrow for the daily limit) and try again.")
        r.raise_for_status()
        data = r.json()
    cand = (data.get("candidates") or [{}])[0]
    text = "".join(p.get("text", "") for p in cand.get("content", {}).get("parts", []))
    meta = data.get("usageMetadata", {})
    usage = {"input_tokens": meta.get("promptTokenCount", 0),
             "output_tokens": meta.get("candidatesTokenCount", 0) + meta.get("thoughtsTokenCount", 0)}
    return text, usage


_claude = None


async def _ask_claude(system, content, max_tokens):
    global _claude
    if _claude is None:
        from anthropic import AsyncAnthropic
        _claude = AsyncAnthropic()
    if not isinstance(content, str):
        content = [{**b, "source": {"type": "base64", **b["source"]}} if b["type"] == "image" else b for b in content]
    resp = await _claude.messages.create(model=MODEL, max_tokens=max_tokens, system=system,
                                         messages=[{"role": "user", "content": content}])
    text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
    return text, {"input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens}


def parse_json(text: str) -> dict:
    """The model is asked for JSON only; this pulls the JSON object out even if extra text slips in."""
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON found in model reply: " + text[:200])
    return json.loads(text[start:end + 1])


def add_usage(total: dict, usage: dict) -> dict:
    total["input_tokens"] = total.get("input_tokens", 0) + usage.get("input_tokens", 0)
    total["output_tokens"] = total.get("output_tokens", 0) + usage.get("output_tokens", 0)
    total["calls"] = total.get("calls", 0) + 1
    return total


def cost_usd(usage: dict) -> float:
    return round(usage.get("input_tokens", 0) / 1e6 * PRICE_IN + usage.get("output_tokens", 0) / 1e6 * PRICE_OUT, 5)
