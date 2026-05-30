from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ChatHistoryMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    mode: str = "chat"
    target_language: str = "en"
    response_length: str = "medium"
    history: Optional[List[ChatHistoryMessage]] = Field(default_factory=list)


class ChatResponse(BaseModel):
    answer: str
    sentiment: Dict[str, Any]
    detected_language: str
    sources: List[Dict[str, Any]] = Field(default_factory=list)
    medical_entities: Dict[str, List[str]] = Field(default_factory=dict)