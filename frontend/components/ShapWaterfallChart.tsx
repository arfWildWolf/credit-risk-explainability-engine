import type { Attribution } from "../src/services/api";

const labels: Record<string, string> = {
  income: "Income",
  credit_score: "Credit score",
  debt_to_income: "Debt-to-income",
  credit_utilization: "Credit utilization",
  delinquencies_2yrs: "Delinquencies",
  loan_amount: "Loan amount",
};

export function ShapWaterfallChart({ attributions }: { attributions: Attribution[] }) {
  const maximum = Math.max(...attributions.map((item) => Math.abs(item.shap_value)), 0.01);
  return (
    <div className="chart" aria-label="SHAP feature attributions">
      {attributions.map((item) => {
        const positive = item.shap_value >= 0;
        return (
          <div className="bar-row" key={item.feature}>
            <span className="bar-label">{labels[item.feature] ?? item.feature}</span>
            <div className="bar-track">
              <div className={`bar ${positive ? "positive" : "negative"}`} style={{ width: `${(Math.abs(item.shap_value) / maximum) * 100}%` }} />
            </div>
            <span className="bar-value">{positive ? "+" : ""}{item.shap_value.toFixed(3)}</span>
          </div>
        );
      })}
    </div>
  );
}