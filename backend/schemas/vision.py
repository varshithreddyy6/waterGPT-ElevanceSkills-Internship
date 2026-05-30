from pydantic import BaseModel


class VisionResponse(BaseModel):
    answer: str
    model: str