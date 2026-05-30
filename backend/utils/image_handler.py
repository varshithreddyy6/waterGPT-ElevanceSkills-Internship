import base64
import io

from PIL import Image

from config import VISION_MODEL_PRIMARY, VISION_MODEL_FALLBACK


class ImageHandler:
    def encode_image(self, image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def encode_pil_image(self, pil_image):
        buffered = io.BytesIO()

        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")

        pil_image.save(buffered, format="JPEG", quality=85)

        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    def process_uploaded_image(self, uploaded_file):
        try:
            return Image.open(uploaded_file)
        except Exception as e:
            print(f"Image processing error: {e}")
            return None

    def _call_vision_model(self, client, image, prompt, model):
        base64_image = self.encode_pil_image(image)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=1024,
        )

        return response.choices[0].message.content

    def describe_image_with_groq(
        self,
        client,
        image,
        prompt="Describe this image in detail",
    ):
        try:
            return self._call_vision_model(
                client,
                image,
                prompt,
                VISION_MODEL_PRIMARY,
            )
        except Exception as e:
            print(f"Primary vision model failed: {e}")

            try:
                return self._call_vision_model(
                    client,
                    image,
                    prompt,
                    VISION_MODEL_FALLBACK,
                )
            except Exception as e2:
                return f"Image analysis error: {str(e2)}"

    def get_image_info(self, image):
        return {
            "format": image.format,
            "size": image.size,
            "mode": image.mode,
        }