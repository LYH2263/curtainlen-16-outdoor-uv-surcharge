import pytest
from app.modules import exposure

CALC = {"meters": 14.25, "panels": 5, "cut_height": 2.85}


def test_indoor_order_equals_base():
    r = exposure.apply(dict(CALC), exposure.INDOOR, {})
    assert r["base_meters"] == 14.25
    assert r["extra_meters"] == 0.0
    assert r["order_meters"] == 14.25
    assert r["exposure_label"] == "普通室内"


def test_outdoor_uv_adds_configured_extra():
    s = {exposure.EXTRA_SETTING_KEY: "0.5", exposure.ENABLED_SETTING_KEY: "1"}
    r = exposure.apply(dict(CALC), exposure.OUTDOOR_UV, s)
    assert r["extra_meters"] == 0.5
    assert r["order_meters"] == 14.75
    assert r["exposure_label"] == "户外抗紫外"


def test_outdoor_uv_default_extra_when_setting_missing():
    r = exposure.apply(dict(CALC), exposure.OUTDOOR_UV, {})
    assert r["extra_meters"] == exposure.DEFAULT_EXTRA_METERS
    assert r["order_meters"] == round(14.25 + exposure.DEFAULT_EXTRA_METERS, 2)


def test_disabled_type_falls_back_to_base():
    s = {exposure.EXTRA_SETTING_KEY: "0.5", exposure.ENABLED_SETTING_KEY: "0"}
    r = exposure.apply(dict(CALC), exposure.OUTDOOR_UV, s)
    assert r["extra_meters"] == 0.0
    assert r["order_meters"] == r["base_meters"]


@pytest.mark.parametrize("bad", ["abc", "-0.5", "nan", "inf", "-inf", "1,5"])
def test_invalid_extra_rejected(bad):
    s = {exposure.EXTRA_SETTING_KEY: bad, exposure.ENABLED_SETTING_KEY: "1"}
    with pytest.raises(exposure.ExposureConfigError):
        exposure.apply(dict(CALC), exposure.OUTDOOR_UV, s)


def test_invalid_extra_ignored_when_disabled():
    s = {exposure.EXTRA_SETTING_KEY: "abc", exposure.ENABLED_SETTING_KEY: "0"}
    r = exposure.apply(dict(CALC), exposure.OUTDOOR_UV, s)
    assert r["order_meters"] == r["base_meters"]


def test_unknown_type_rejected():
    with pytest.raises(exposure.ExposureConfigError):
        exposure.apply(dict(CALC), "moonlight", {})


def test_catalog_marks_invalid_config_without_crashing():
    items = exposure.catalog({exposure.EXTRA_SETTING_KEY: "abc"})
    uv = [t for t in items if t["key"] == exposure.OUTDOOR_UV][0]
    assert uv["config_error"]
    indoor = [t for t in items if t["key"] == exposure.INDOOR][0]
    assert indoor["enabled"] is True and indoor["extra_meters"] == 0.0
