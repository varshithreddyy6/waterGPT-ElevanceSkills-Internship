from fastapi import APIRouter, UploadFile, File, HTTPException

from services.voice_service import transcribe_audio


router = APIRouter(
    prefix="/voice",
    tags=["voice"],
)


@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    try:
        audio_bytes = await file.read()

        return transcribe_audio(
            audio_bytes=audio_bytes,
            filename=file.filename or "audio.webm",
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )