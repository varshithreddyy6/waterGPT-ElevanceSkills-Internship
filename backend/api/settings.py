from fastapi import APIRouter

from services.settings_service import languages


router = APIRouter(
    prefix="/settings",
    tags=["settings"],
)


@router.get("/languages")
def get_languages():
    return languages()