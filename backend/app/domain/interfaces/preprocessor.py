"""Preprocessing abstraction reserved for production feature pipelines."""

from abc import ABC, abstractmethod

import numpy as np


class BasePreprocessor(ABC):
    """Port for transforming validated domain input into model features."""

    @abstractmethod
    def transform(self, features: np.ndarray) -> np.ndarray:
        """Transform raw features without changing row semantics."""
