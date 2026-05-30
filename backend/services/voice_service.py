import tempfile
from pathlib import Path

from core.groq_client import client


VOICE_MODEL_PRIMARY = "whisper-large-v3"
VOICE_MODEL_FALLBACK = "whisper-large-v3-turbo"


def transcribe_audio(audio_bytes: bytes, filename: str = "audio.webm"):
    suffix = Path(filename).suffix or ".webm"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
        temp_audio.write(audio_bytes)
        temp_audio_path = temp_audio.name

    try:
        with open(temp_audio_path, "rb") as audio_file:
            try:
                transcription = client.audio.transcriptions.create(
                    file=(filename, audio_file),
                    model=VOICE_MODEL_PRIMARY,
                    response_format="json",
                )
            except Exception:
                audio_file.seek(0)
                transcription = client.audio.transcriptions.create(
                    file=(filename, audio_file),
                    model=VOICE_MODEL_FALLBACK,
                    response_format="json",
                )

        text = getattr(transcription, "text", "")

        return {
            "text": text,
            "model": VOICE_MODEL_PRIMARY,
        }

    finally:
        try:
            Path(temp_audio_path).unlink(missing_ok=True)
        except Exception:
            pass