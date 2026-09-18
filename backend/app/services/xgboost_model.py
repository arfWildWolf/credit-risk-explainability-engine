"""XGBoost model adapter with an out-of-the-box fallback model."""

from pathlib import Path

import joblib
import numpy as np
from xgboost import XGBClassifier

from app.domain.interfaces.model import BaseCreditModel


class XGBoostCreditModel(BaseCreditModel):
    """Load a persisted classifier or train a deterministic demo classifier."""

    feature_names = (
        "income",
        "credit_score",
        "debt_to_income",
        "credit_utilization",
        "delinquencies_2yrs",
        "loan_amount",
    )

    def __init__(self, model_path: str | Path = "models/credit_risk_model.joblib") -> None:
        self.model_path = Path(model_path)
        self.model = self._load_or_train()

    def _load_or_train(self) -> XGBClassifier:
        if self.model_path.is_file():
            return joblib.load(self.model_path)

        rng = np.random.default_rng(42)
        features = np.column_stack(
            [
                rng.uniform(25_000, 200_000, 2500),
                rng.uniform(300, 850, 2500),
                rng.uniform(0, 1, 2500),
                rng.uniform(0, 1, 2500),
                rng.poisson(0.35, 2500),
                rng.uniform(5_000, 100_000, 2500),
            ]
        )
        risk_score = (
            -1.2
            - 0.000004 * features[:, 0]
            - 0.006 * (features[:, 1] - 600)
            + 3.0 * features[:, 2]
            + 2.0 * features[:, 3]
            + 0.65 * features[:, 4]
            + 0.000006 * features[:, 5]
        )
        default_probability = 1 / (1 + np.exp(-risk_score))
        labels = rng.binomial(1, default_probability)
        model = XGBClassifier(
            n_estimators=80,
            max_depth=3,
            learning_rate=0.08,
            subsample=0.9,
            colsample_bytree=0.9,
            eval_metric="logloss",
            random_state=42,
            n_jobs=1,
        )
        model.fit(features, labels)
        return model

    def predict_proba(self, features: np.ndarray) -> float:
        """Predict default probability for one row."""

        values = np.asarray(features, dtype=float).reshape(1, -1)
        return float(self.model.predict_proba(values)[0, 1])