from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.modules import exposure
from app.repositories import settings_repo
router = APIRouter()

ALLOWED_KEYS = {"default_fullness"} | exposure.SETTING_KEYS

class SettingUpdate(BaseModel):
    key: str
    value: str

@router.get("/settings")
def settings(): return settings_repo.get_all()

@router.post("/settings")
def update_setting(body: SettingUpdate):
    if body.key not in ALLOWED_KEYS:
        raise HTTPException(400, f"unknown setting: {body.key}")
    settings_repo.set(body.key, body.value)
    return settings_repo.get_all()
