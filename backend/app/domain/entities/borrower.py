"""Validated borrower input."""

from pydantic import BaseModel, Field


class BorrowerRequest(BaseModel):
    """Features accepted by the credit risk model."""

    income: float = Field(gt=0)
    credit_score: int = Field(ge=300, le=850)
    debt_to_income: float = Field(ge=0, le=1)
    credit_utilization: float = Field(ge=0, le=1)
    delinquencies_2yrs: int = Field(ge=0)
    loan_amount: float = Field(gt=0)

    def as_features(self) -> list[float]:
        """Return values in the model's stable feature order."""

        return [
            self.income,
            self.credit_score,
            self.debt_to_income,
            self.credit_utilization,
            self.delinquencies_2yrs,
            self.loan_amount,
        ]