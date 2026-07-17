"""
Gemini AI client wrapper for waterGPT.

This module centralizes all interaction with Google's Gemini API
(via the official `google-genai` SDK) for the Multi-Modal Chatbot task.

It is used for:
    - Vision understanding (image -> text)      : gemini-2.5-flash
    - Image generation      (text -> image)      : gemini-2.5-flash-image
    - Image editing         (image + text -> image): gemini-2.5-flash-image

The client is created lazily so the backend can still start even if
GEMINI_API_KEY has not been configured yet (the vision/image endpoints
will simply raise a clear, actionable error at request time instead of
crashing the whole application at import time).
"""

from google import genai

from config import GEMINI_API_KEY


_client = None


def get_gemini_client():
    """Returns a cached google-genai Client instance."""
    global _client

    if _client is None:
        if not GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Add it to backend/.env "
                "(see backend/.env.example) to enable Gemini-powered "
                "vision understanding and image generation."
            )

        _client = genai.Client(api_key=GEMINI_API_KEY)

    return _client