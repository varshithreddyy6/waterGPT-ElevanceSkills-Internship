from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse

from config import GENERATED_IMAGES_DIR
from schemas.vision import ImageGenerationRequest
from services.vision_service import (
    analyze_image,
    generate_image_from_text,
    edit_image_with_text,
)


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
    """Image Understanding: upload an image, ask a question about it (Gemini)."""
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


@router.post("/generate")
def generate(req: ImageGenerationRequest):
    """Image Generation: create a brand-new image from a text prompt (Gemini)."""
    try:
        return generate_image_from_text(
            prompt=req.prompt,
            target_language=req.target_language,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.post("/edit")
async def edit(
    prompt: str = Form(...),
    target_language: str = Form("en"),
    image: UploadFile = File(...),
):
    """Image Editing: upload an image + instruction, get back an edited image (Gemini)."""
    try:
        image_bytes = await image.read()

        return edit_image_with_text(
            image_bytes=image_bytes,
            prompt=prompt,
            target_language=target_language,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.get("/generated/{filename}")
def get_generated_image(filename: str):
    """Serves a Gemini-generated image back to the frontend."""
    filepath = GENERATED_IMAGES_DIR / filename

    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Image not found.")

    return FileResponse(filepath, media_type="image/png")