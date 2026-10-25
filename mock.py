"""Fake Claude replies, used only when MOCK_LLM=1 for offline testing. Not used on Vercel."""
import json
import random
import re

import prompts


def reply(system, content):
    usage = {"input_tokens": 800, "output_tokens": 200}
    if system == prompts.TRANSCRIBE:
        return json.dumps({"text": "Mock transcription of a handwritten answer.", "legibility": "clear",
                           "unclear_words": 0}), usage
    if system == prompts.LEARN:
        return json.dumps({"dos": ["Give credit for a correct classroom example."],
                           "donts": ["Don't give marks for only repeating the question."],
                           "notes": "Mock rules."}), usage
    # scoring: score depends a little on length, with small random noise
    text = content if isinstance(content, str) else ""
    doc = text.split("<<<")[-1]
    base = min(5, len(re.findall(r"\w+", doc)) // 25)
    total = max(0, min(5, base + random.choice([0, 0, 0, 1, -1])))
    return json.dumps({"criteria": [{"criterion": "Overall", "score": total, "max": 5,
                                     "evidence": doc.strip()[:40], "reason": "Mock reason."}],
                       "total": total, "max_total": 5, "summary": "Mock summary."}), usage
