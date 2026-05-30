import io

from fastapi import APIRouter, UploadFile, File, HTTPException

from schemas.knowledge import UrlKnowledgeRequest, TextKnowledgeRequest
from services import knowledge_service


router = APIRouter(
    prefix="/knowledge",
    tags=["knowledge"],
)


def extract_text_from_pdf(file_bytes: bytes):
    try:
        from pypdf import PdfReader

        reader = PdfReader(io.BytesIO(file_bytes))
        text_parts = []

        for page in reader.pages:
            page_text = page.extract_text() or ""
            if page_text.strip():
                text_parts.append(page_text)

        return "\n\n".join(text_parts)

    except Exception as e:
        raise ValueError(f"Could not read PDF: {e}")


@router.get("/stats")
def stats():
    return knowledge_service.stats()


@router.post("/url")
def add_url(req: UrlKnowledgeRequest):
    try:
        count = knowledge_service.add_url(req.url)

        return {
            "added_chunks": count,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.post("/text")
def add_text(req: TextKnowledgeRequest):
    try:
        count = knowledge_service.add_text(req.text)

        return {
            "added_chunks": count,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.post("/file")
async def add_file(file: UploadFile = File(...)):
    try:
        content = await file.read()

        filename = file.filename or "uploaded_file"
        lower_name = filename.lower()

        if lower_name.endswith(".pdf"):
            text = extract_text_from_pdf(content)
        else:
            text = content.decode(
                "utf-8",
                errors="ignore",
            )

        if not text.strip():
            return {
                "filename": filename,
                "added_chunks": 0,
                "message": "No readable text found in file.",
            }

        count = knowledge_service.add_file_text(
            filename,
            text,
        )

        return {
            "filename": filename,
            "added_chunks": count,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.delete("/clear")
def clear():
    return knowledge_service.clear()