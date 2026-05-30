from fastapi import APIRouter

from services.analytics_service import empty_stats


router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
)


@router.get("")
def analytics():
    return empty_stats()