from fastapi import HTTPException
from app.engines.curtain_math import fabric_meters
from app.modules import exposure
from app.repositories import fabrics, history, settings_repo, windows

def run_estimate(window_id: int, fabric_id: int, save: bool, note: str, exposure_type: str = exposure.INDOOR):
    w = windows.get_window(window_id)
    f = fabrics.get_fabric(fabric_id)
    if not w or not f:
        raise HTTPException(404, "not found")
    if w.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty window")
    if not exposure.is_valid_type(exposure_type):
        raise HTTPException(422, f"unknown exposure type: {exposure_type}")
    settings = settings_repo.get_all()
    fullness = float(w.get("fullness") or settings.get("default_fullness", 2.0))
    calc = fabric_meters(w["width"], w["height"], fullness, f["hem_top"], f["hem_bottom"], f["fabric_width"])
    try:
        result = exposure.apply(calc, exposure_type, settings)
    except exposure.ExposureConfigError as e:
        raise HTTPException(422, str(e))
    # 落库的是含类型与订货米的快照；事后改默认加米不会重算旧编号
    run_id = history.insert_run(window_id, fabric_id, result, note) if save else None
    return {"window": w, "fabric": f, "run_id": run_id, **result}
