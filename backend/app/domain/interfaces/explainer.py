"""Model explanation abstraction."""

from abc import ABC, abstractmethod
from typing import Any

import numpy as np


class BaseExplainer(ABC):
    """Port for feature attribution providers."""

    @abstractmethod
    def explain(self, model: Any, features: np.ndarray) -> dict[str, Any]:
        """Return a base value and ordered feature attributions."""
