"""空间曝晒类型模块：类型枚举、加米规则、展示目录。

- indoor（普通室内）：订货米 = 基础米
- outdoor_uv（户外抗紫外）：订货米 = 基础米 + 固定加米（设置页可配）

加米配置存于 settings 表（本模块持有键名与默认值），测算时读取并校验；
非法配置（非数字 / 负数 / 非有限值）抛 ExposureConfigError，由服务层转为拒绝测算。
类型停用后，新测算回到基础口径（加米为 0），已落库的历史快照不受影响。
"""
import math

INDOOR = "indoor"
OUTDOOR_UV = "outdoor_uv"

# 类型枚举与展示标签（历史页/算料台经接口取用，前端不写死）
EXPOSURE_TYPES = {
    INDOOR: {"label": "普通室内"},
    OUTDOOR_UV: {"label": "户外抗紫外"},
}

EXTRA_SETTING_KEY = "exposure_outdoor_uv_extra"
ENABLED_SETTING_KEY = "exposure_outdoor_uv_enabled"
SETTING_KEYS = {EXTRA_SETTING_KEY, ENABLED_SETTING_KEY}

DEFAULT_EXTRA_METERS = 0.5
DEFAULT_ENABLED = True

_TRUTHY = {"1", "true", "yes", "on"}
_FALSY = {"0", "false", "no", "off"}


class ExposureConfigError(ValueError):
    """加米配置非法（测算应被拒绝）。"""


def is_valid_type(exposure_type) -> bool:
    return exposure_type in EXPOSURE_TYPES


def label_of(exposure_type: str) -> str:
    return EXPOSURE_TYPES[exposure_type]["label"]


def outdoor_uv_enabled(settings: dict) -> bool:
    raw = str(settings.get(ENABLED_SETTING_KEY, "")).strip().lower()
    if raw in _TRUTHY:
        return True
    if raw in _FALSY:
        return False
    return DEFAULT_ENABLED


def configured_extra(settings: dict) -> float:
    """读取固定加米；非法配置抛 ExposureConfigError。"""
    raw = str(settings.get(EXTRA_SETTING_KEY, "")).strip()
    if raw == "":
        return DEFAULT_EXTRA_METERS
    try:
        extra = float(raw)
    except (TypeError, ValueError):
        raise ExposureConfigError(f"invalid exposure extra: {raw!r}")
    if not math.isfinite(extra) or extra < 0:
        raise ExposureConfigError(f"invalid exposure extra: {raw!r}")
    return extra


def apply(calc: dict, exposure_type: str, settings: dict) -> dict:
    """在基础测算结果上叠加曝晒类型口径，返回含订货米的完整结果。"""
    if not is_valid_type(exposure_type):
        raise ExposureConfigError(f"unknown exposure type: {exposure_type!r}")
    base = float(calc["meters"])
    extra = 0.0
    if exposure_type == OUTDOOR_UV and outdoor_uv_enabled(settings):
        extra = configured_extra(settings)
    return {
        **calc,
        "exposure_type": exposure_type,
        "exposure_label": label_of(exposure_type),
        "base_meters": round(base, 2),
        "extra_meters": round(extra, 3),
        "order_meters": round(base + extra, 2),
    }


def catalog(settings: dict) -> list:
    """算料台可选类型目录；配置非法时如实标记而不崩溃。"""
    extra, config_error = 0.0, None
    try:
        extra = configured_extra(settings)
    except ExposureConfigError as e:
        config_error = str(e)
    return [
        {"key": INDOOR, "label": label_of(INDOOR), "enabled": True, "extra_meters": 0.0},
        {
            "key": OUTDOOR_UV,
            "label": label_of(OUTDOOR_UV),
            "enabled": outdoor_uv_enabled(settings),
            "extra_meters": extra,
            "config_error": config_error,
        },
    ]
