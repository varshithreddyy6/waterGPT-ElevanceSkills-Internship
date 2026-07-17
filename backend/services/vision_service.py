import io

from PIL import Image

from core.state import translator, gemini_vision


def analyze_image(
    image_bytes: bytes,
    question: str,
    target_language="en",
    history="",
):
    image = Image.open(io.BytesIO(image_bytes))

    final_prompt = question

    if history:
        final_prompt = (
            "You are continuing a visual conversation about the same image.\n\n"
            f"Previous conversation:\n{history}\n\n"
            f"New question: {question}"
        )

    answer = gemini_vision.describe_image(image, final_prompt)

    if target_language != "en":
        answer = translator.translate_from_english(
            answer,
            target_language,
        )

    return {
        "answer": answer,
        "model": "Google Gemini (gemini-2.5-flash)",
    }


def generate_image_from_text(prompt: str, target_language="en"):
    result = gemini_vision.generate_image(prompt)

    caption = result.get("text") or "Here is the image I generated."

    if target_language != "en":
        caption = translator.translate_from_english(caption, target_language)

    return {
        "answer": caption,
        "image_url": result["url"],
        "model": "Google Gemini (gemini-2.5-flash-image)",
    }


def edit_image_with_text(image_bytes: bytes, prompt: str, target_language="en"):
    image = Image.open(io.BytesIO(image_bytes))

    result = gemini_vision.edit_image(image, prompt)

    caption = result.get("text") or "Here is your edited image."

    if target_language != "en":
        caption = translator.translate_from_english(caption, target_language)

    return {
        "answer": caption,
        "image_url": result["url"],
        "model": "Google Gemini (gemini-2.5-flash-image)",
    }