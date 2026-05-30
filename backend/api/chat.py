from fastapi import APIRouter, HTTPException

from schemas.chat import ChatRequest, ChatResponse
from services.chat_service import handle_chat


router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post("", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        return handle_chat(
            message=req.message,
            mode=req.mode,
            target_language=req.target_language,
            response_length=req.response_length,
            history=req.history or [],
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )