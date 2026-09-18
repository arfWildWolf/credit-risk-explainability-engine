"""Credit risk banding and adverse action language."""

from collections.abc import Sequence


class RiskDecisionEngine:
    """Translate model output into consistent product decisions."""

    _labels = {
        "income": "lower income",
        "credit_score": "lower credit score",
        "debt_to_income": "higher debt-to-income ratio",
        "credit_utilization": "higher credit utilization",
        "delinquencies_2yrs": "recent payment delinquencies",
        "loan_amount": "larger requested loan amount",
    }

    def risk_band(self, probability: float) -> str:
        if probability < 0.10:
            return "Low"
        if probability <= 0.25:
            return "Medium"
        return "High"

    def adverse_reasons(self, attributions: Sequence[dict[str, float | str]]) -> list[str]:
        positive = sorted(
            (item for item in attributions if float(item["shap_value"]) > 0),
            key=lambda item: float(item["shap_value"]),
            reverse=True,
        )
        return [f"{self._labels.get(str(item['feature']), str(item['feature']))} increased estimated risk."
                for item in positive[:2]]