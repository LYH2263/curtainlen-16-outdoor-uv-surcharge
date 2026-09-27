from fastapi import APIRouter
from app.modules.exposure import display
from app.repositories import history as repo
router = APIRouter()
@router.get("/runs")
def runs(limit: int = 50):
    items = repo.list_runs(limit)
    for it in items:
        it["exposure"] = display.summarize_run(it["result"])
    return {"items": items}
