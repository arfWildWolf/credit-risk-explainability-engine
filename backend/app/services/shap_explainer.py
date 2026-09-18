"""SHAP tree explanation adapter."""

from typing import Any

import numpy as np
import shap

from app.domain.interfaces.explainer import BaseExplainer


class SHAPTreeExplainer(BaseExplainer):
    """Explain tree model output in the positive-class probability space."""

    def __init__(self, feature_names: tuple[str, ...]) -> None:
        self.feature_names = feature_names

    def explain(self, model: Any, features: np.ndarray) -> dict[str, Any]:
        values = np.asarray(features, dtype=float).reshape(1, -1)
        explanation = shap.TreeExplainer(model).shap_values(values)
        if isinstance(explanation, list):
            shap_values = np.asarray(explanation[-1][0], dtype=float)
        else:
            shap_values = np.asarray(explanation[0], dtype=float)

        base_values = shap.TreeExplainer(model).expected_value
        if isinstance(base_values, (list, np.ndarray)):
            base_value = float(np.asarray(base_values).reshape(-1)[-1])
        else:
            base_value = float(base_values)

        attributions = [
            {"feature": name, "shap_value": float(value)}
            for name, value in zip(self.feature_names, shap_values, strict=True)
        ]
        attributions.sort(key=lambda item: abs(item["shap_value"]), reverse=True)
        return {"base_value": base_value, "attributions": attributions}