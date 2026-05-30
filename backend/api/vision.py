from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from services.vision_service import analyze_image


router = APIRouter(
    prefix="/vision",
    tags=["vision"],
)


@router.post("")
async def vision(
    question: str = Form(...),
    target_language: str = Form("en"),
    history: str = Form(""),
    image: UploadFile = File(...),
):
    try:
        image_bytes = await image.read()

        return analyze_image(
            image_bytes=image_bytes,
            question=question,
            target_language=target_language,
            history=history,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )