from pydantic import BaseModel


class SentimentStats(BaseModel):
    positive: int = 0
    neutral: int = 0
    negative: int = 0