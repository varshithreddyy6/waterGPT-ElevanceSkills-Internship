from pydantic import BaseModel


class VisionResponse(BaseModel):
    answer: str
    model: str


class ImageGenerationRequest(BaseModel):
    prompt: str
    target_language: str = "en"


class ImageGenerationResponse(BaseModel):
    answer: str
    image_url: str
    model: str