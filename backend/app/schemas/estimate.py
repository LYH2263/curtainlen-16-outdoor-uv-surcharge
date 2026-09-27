from pydantic import BaseModel
from app.modules import exposure

class EstimateRequest(BaseModel):
    window_id: int
    fabric_id: int
    save: bool = False
    note: str = ""
    exposure_type: str = exposure.INDOOR
