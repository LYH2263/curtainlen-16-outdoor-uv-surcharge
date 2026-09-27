import pytest
from fastapi import HTTPException
from app import seed
from app.modules import exposure
from app.repositories import history, settings_repo
from app.services import estimate_service

seed.init_db()


def _set(extra=None, enabled=None):
    if extra is not None:
        settings_repo.set(exposure.EXTRA_SETTING_KEY, extra)
    if enabled is not None:
        settings_repo.set(exposure.ENABLED_SETTING_KEY, enabled)


def test_outdoor_uv_saved_run_pins_type_and_order_meters():
    _set(extra="0.5", enabled="1")
    r = estimate_service.run_estimate(1, 1, True, "", exposure.OUTDOOR_UV)
    assert r["run_id"]
    assert r["base_meters"] == 14.25 and r["extra_meters"] == 0.5 and r["order_meters"] == 14.75
    # 事后改默认加米：旧编号不得重算，新测算用新口径
    _set(extra="3.0")
    saved = [x for x in history.list_runs() if x["id"] == r["run_id"]][0]
    assert saved["result"]["exposure_type"] == exposure.OUTDOOR_UV
    assert saved["result"]["extra_meters"] == 0.5
    assert saved["result"]["order_meters"] == 14.75
    fresh = estimate_service.run_estimate(1, 1, False, "", exposure.OUTDOOR_UV)
    assert fresh["extra_meters"] == 3.0 and fresh["order_meters"] == 17.25


def test_indoor_unaffected_by_extra_config():
    _set(extra="0.5", enabled="1")
    r = estimate_service.run_estimate(1, 1, False, "", exposure.INDOOR)
    assert r["extra_meters"] == 0.0 and r["order_meters"] == r["base_meters"]


def test_invalid_extra_config_rejects_estimate():
    _set(extra="abc", enabled="1")
    with pytest.raises(HTTPException) as ei:
        estimate_service.run_estimate(1, 1, False, "", exposure.OUTDOOR_UV)
    assert ei.value.status_code == 422


def test_disabled_type_new_estimate_back_to_base():
    _set(extra="0.5", enabled="0")
    r = estimate_service.run_estimate(1, 1, False, "", exposure.OUTDOOR_UV)
    assert r["extra_meters"] == 0.0 and r["order_meters"] == r["base_meters"]


def test_unknown_exposure_type_rejected():
    _set(extra="0.5", enabled="1")
    with pytest.raises(HTTPException) as ei:
        estimate_service.run_estimate(1, 1, False, "", "moonlight")
    assert ei.value.status_code == 422
