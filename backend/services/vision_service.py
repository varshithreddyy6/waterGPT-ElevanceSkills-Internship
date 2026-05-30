import io

from PIL import Image

from core.groq_client import client
from core.state import image_handler, translator


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

    answer = image_handler.describe_image_with_groq(
        client,
        image,
        final_prompt,
    )

    if target_language != "en":
        answer = translator.translate_from_english(
            answer,
            target_language,
        )

    return {
        "answer": answer,
        "model": "Groq Vision",
    }