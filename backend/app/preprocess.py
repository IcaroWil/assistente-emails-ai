import re
import string

EMAIL_RE = re.compile(r"\b\S+@\S+\.\S+\b", re.I)
URL_RE = re.compile(r"http\S+|www\.\S+", re.I)

def clean_text(text: str) -> str:
    text = text or ""
    text = strip_quoted(text)
    text = text.lower()
    text = URL_RE.sub("", text)
    text = EMAIL_RE.sub("", text)
    text = text.replace("\r", " ")
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = " ".join(text.split())
    return text.strip()

def strip_quoted(text: str) -> str:
    return "\n".join(line for line in text.splitlines() if not line.strip().startswith(">"))
