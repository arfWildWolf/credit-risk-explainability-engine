"""Credit model abstraction."""

from abc import ABC, abstractmethod

import numpy as np


class BaseCreditModel(ABC):
    """Port for a binary credit risk model."""

    feature_names: tuple[str, ...] = ()

    @abstractmethod
    def predict_proba(self, features: np.ndarray) -> float:
        """Return the probability of default for one feature row."""
