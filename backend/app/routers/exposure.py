from fastapi import APIRouter
from app.modules import exposure
from app.repositories import settings_repo
router = APIRouter()
@router.get("/exposure/types")
def exposure_types():
    return {"items": exposure.catalog(settings_repo.get_all())}
