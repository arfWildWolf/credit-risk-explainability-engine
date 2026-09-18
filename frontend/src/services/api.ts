export type BorrowerPayload = {
  income: number;
  credit_score: number;
  debt_to_income: number;
  credit_utilization: number;
  delinquencies_2yrs: number;
  loan_amount: number;
};

export type Attribution = { feature: string; shap_value: number };

export type CreditRiskResult = {
  default_probability: number;
  risk_band: string;
  base_value: number;
  attributions: Attribution[];
  adverse_reasons: string[];
};

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "";

export async function predictCreditRisk(payload: BorrowerPayload): Promise<CreditRiskResult> {
  const response = await fetch(`${apiBaseUrl}/api/v1/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error("The risk service could not score this borrower.");
  }

  return response.json() as Promise<CreditRiskResult>;
}