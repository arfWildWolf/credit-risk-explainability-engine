"""Credit prediction endpoint."""

from functools import lru_cache

import numpy as np
from fastapi import APIRouter, Depends, HTTPException

from app.core.config import get_settings
from app.domain.entities.borrower import BorrowerRequest
from app.domain.entities.prediction import CreditRiskResponse
from app.services.risk_decision_engine import RiskDecisionEngine
from app.services.shap_explainer import SHAPTreeExplainer
from app.services.xgboost_model import XGBoostCreditModel

router = APIRouter(tags=["prediction"])


@lru_cache
def get_model() -> XGBoostCreditModel:
    return XGBoostCreditModel(get_settings().model_path)


@lru_cache
def get_explainer() -> SHAPTreeExplainer:
    return SHAPTreeExplainer(get_model().feature_names)


def get_decision_engine() -> RiskDecisionEngine:
    return RiskDecisionEngine()


@router.post("/predict", response_model=CreditRiskResponse)
def predict(
    borrower: BorrowerRequest,
    model: XGBoostCreditModel = Depends(get_model),
    explainer: SHAPTreeExplainer = Depends(get_explainer),
    decision_engine: RiskDecisionEngine = Depends(get_decision_engine),
) -> CreditRiskResponse:
    """Score one borrower and return an explainable decision."""

    try:
        features = np.asarray(borrower.as_features(), dtype=float)
        probability = model.predict_proba(features)
        explanation = explainer.explain(model.model, features)
        attributions = explanation["attributions"]
        return CreditRiskResponse(
            default_probability=probability,
            risk_band=decision_engine.risk_band(probability),
            base_value=explanation["base_value"],
            attributions=attributions,
            adverse_reasons=decision_engine.adverse_reasons(attributions),
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Unable to generate a credit explanation") from exc