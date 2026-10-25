"""Removes personal details from typed text BEFORE it is sent to Claude."""
import re

PATTERNS = [
    (re.compile(r"\b\d{5}-\d{7}-\d\b"), "[CNIC]"),
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "[EMAIL]"),
    (re.compile(r"(\+92[\s-]?|0)3\d{2}[\s-]?\d{7}\b"), "[PHONE]"),
]

# Whole lines that start with these labels are replaced (common on Pakistani CVs and answer sheets)
LABELS = re.compile(
    r"^\s*(name|student name|candidate name|father'?s name|roll\s*(no|number)\.?|cnic|"
    r"date of birth|dob|age|gender|sex|marital status|religion|address|phone|mobile|email)\s*[:\-].*$",
    re.I | re.M,
)


def redact(text: str) -> tuple[str, int]:
    """Returns (clean_text, number_of_items_removed)."""
    count = 0
    text, n = LABELS.subn(lambda m: m.group(1).title() + ": [REDACTED]", text)
    count += n
    for pat, repl in PATTERNS:
        text, n = pat.subn(repl, text)
        count += n
    return text, count
