"""Shared deterministic text extraction and tokenization."""
from __future__ import annotations
import re
from typing import Any

_TOKEN = re.compile(r"[a-z0-9]+(?:['-][a-z0-9]+)*")

def document_text(document: dict[str, Any], fields: str = "title_abstract") -> str:
    """Join BEIR title/text fields with stable spacing; optionally title only."""
    title = str(document.get("title") or "").strip()
    text = str(document.get("text") or "").strip()
    if fields == "title":
        return title
    if fields != "title_abstract":
        raise ValueError(f"Unsupported text fields: {fields}")
    return " ".join(part for part in (title, text) if part)

def tokenize(text: str) -> list[str]:
    """Lowercase alphanumeric tokenizer shared by queries and BM25 corpus."""
    return _TOKEN.findall(text.lower())
