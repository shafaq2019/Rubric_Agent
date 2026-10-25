"""Talks to Claude. Every call returns (text, usage) so we can count tokens and cost."""
import json
import os
import re

MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5")
# Price per million tokens (USD). Check the current price on anthropic.com/pricing
# and change these in Vercel settings if needed.
PRICE_IN = float(os.getenv("PRICE_IN_PER_MTOK", "3"))
PRICE_OUT = float(os.getenv("PRICE_OUT_PER_MTOK", "15"))
MOCK = os.getenv("MOCK_LLM") == "1"  # used only for offline testing

_client = None


def _get_client():
    global _client
    if _client is None:
        from anthropic import AsyncAnthropic
        _client = AsyncAnthropic()  # reads ANTHROPIC_API_KEY from the environment
    return _client


async def ask(system: str, content, max_tokens: int = 1500):
    """Send one message to Claude. `content` is a string or a list of content blocks."""
    if MOCK:
        from core import mock
        return mock.reply(system, content)
    resp = await _get_client().messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": content}],
    )
    text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
    usage = {"input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens}
    return text, usage


def parse_json(text: str) -> dict:
    """Claude is asked for JSON only; this pulls the JSON object out even if extra text slips in."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.M).strip()
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
