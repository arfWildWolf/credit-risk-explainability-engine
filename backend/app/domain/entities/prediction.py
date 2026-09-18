"""Prediction response models."""

from pydantic import BaseModel, Field


class ShapAttribution(BaseModel):
    """One feature's contribution to the model prediction."""

    feature: str
    shap_value: float


class CreditRiskResponse(BaseModel):
    """Prediction, explanation, and human-readable decision context."""

    default_probability: float = Field(ge=0, le=1)
    risk_band: str
    base_value: float
    attributions: list[ShapAttribution]
    adverse_reasons: list[str]