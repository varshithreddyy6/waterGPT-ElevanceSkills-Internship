"""
Gemini-powered multi-modal handler.
"""

import io
import uuid

from PIL import Image
from google.genai import types

from config import GEMINI_VISION_MODEL, GEMINI_IMAGE_MODEL, GENERATED_IMAGES_DIR
from core.gemini_client import get_gemini_client


class GeminiVisionHandler:
    def pil_to_bytes(self, pil_image, fmt="JPEG"):
        buffer = io.BytesIO()

        if pil_image.mode != "RGB" and fmt == "JPEG":
            pil_image = pil_image.convert("RGB")

        pil_image.save(buffer, format=fmt)

        return buffer.getvalue()

    def describe_image(self, pil_image, prompt="Describe this image in detail."):
        client = get_gemini_client()

        image_bytes = self.pil_to_bytes(pil_image, fmt="JPEG")

        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type="image/jpeg",
        )

        response = client.models.generate_content(
            model=GEMINI_VISION_MODEL,
            contents=[image_part, prompt],
        )

        text = getattr(response, "text", None)

        if not text:
            raise RuntimeError("Gemini returned an empty response for image understanding.")

        return text

    def generate_image(self, prompt):
        client = get_gemini_client()

        response = client.models.generate_content(
            model=GEMINI_IMAGE_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            ),
        )

        return self._extract_image_response(response)

    def edit_image(self, pil_image, prompt):
        client = get_gemini_client()

        image_bytes = self.pil_to_bytes(pil_image, fmt="PNG")

        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type="image/png",
        )

        response = client.models.generate_content(
            model=GEMINI_IMAGE_MODEL,
            contents=[image_part, prompt],
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            ),
        )

        return self._extract_image_response(response)

    def _extract_image_response(self, response):
        text_out = ""
        saved_path = None

        candidates = getattr(response, "candidates", None) or []

        for candidate in candidates:
            parts = getattr(candidate.content, "parts", None) or []

            for part in parts:
                inline_data = getattr(part, "inline_data", None)

                if inline_data is not None and inline_data.data:
                    image = Image.open(io.BytesIO(inline_data.data))

                    filename = f"{uuid.uuid4().hex}.png"
                    GENERATED_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
                    filepath = GENERATED_IMAGES_DIR / filename

                    image.save(filepath, format="PNG")

                    saved_path = filename

                elif getattr(part, "text", None):
                    text_out += part.text

        if not saved_path:
            raise RuntimeError(
                "Gemini did not return an image. "
                f"Model text response: {text_out or '(empty)'}"
            )

        return {
            "filename": saved_path,
            "url": f"/vision/generated/{saved_path}",
            "text": text_out.strip(),
        }