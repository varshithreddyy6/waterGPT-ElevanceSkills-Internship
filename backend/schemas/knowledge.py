from pydantic import BaseModel


class UrlKnowledgeRequest(BaseModel):
    url: str


class TextKnowledgeRequest(BaseModel):
    text: str