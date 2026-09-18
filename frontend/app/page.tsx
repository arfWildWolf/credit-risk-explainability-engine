"use client";

import { FormEvent, useState } from "react";
import { ShapWaterfallChart } from "../components/ShapWaterfallChart";

type FormData = { income: string; credit_score: string; debt_to_income: string; credit_utilization: string; delinquencies_2yrs: string; loan_amount: string };
type Result = { default_probability: number; risk_band: string; base_value: number; attributions: { feature: string; shap_value: number }[]; adverse_reasons: string[] };

const initialForm: FormData = { income: "85000", credit_score: "720", debt_to_income: "0.28", credit_utilization: "0.32", delinquencies_2yrs: "0", loan_amount: "18000" };
const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function Home() {
  const [form, setForm] = useState<FormData>(initialForm);
  const [result, setResult] = useState<Result | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function updateField(field: keyof FormData, value: string) { setForm((current) => ({ ...current, [field]: value })); }

  async function submit(event: FormEvent) {
    event.preventDefault(); setLoading(true); setError("");
    try {
      const response = await fetch(`${apiUrl}/api/v1/predict`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(Object.fromEntries(Object.entries(form).map(([key, value]) => [key, Number(value)]))) });
      if (!response.ok) throw new Error("The risk service could not score this borrower.");
      setResult(await response.json());
    } catch (requestError) { setError(requestError instanceof Error ? requestError.message : "Something went wrong."); }
    finally { setLoading(false); }
  }

  const fields: { key: keyof FormData; label: string; step: string }[] = [
    { key: "income", label: "Annual income", step: "1000" }, { key: "credit_score", label: "Credit score", step: "1" },
    { key: "debt_to_income", label: "Debt-to-income ratio", step: "0.01" }, { key: "credit_utilization", label: "Credit utilization", step: "0.01" },
    { key: "delinquencies_2yrs", label: "Delinquencies, 2 years", step: "1" }, { key: "loan_amount", label: "Requested loan amount", step: "1000" },
  ];

  return <main className="shell"><div className="dashboard">
    <header className="hero"><div><div className="eyebrow">Risk lens / decision intelligence</div><h1>See the story behind a credit decision.</h1></div><p>Explainable scoring for clearer lending conversations. Every result comes with the factors that moved it.</p></header>
    <div className="grid"><section className="panel"><h2>Borrower profile</h2><form className="form-grid" onSubmit={submit}>{fields.map((field) => <div className="field" key={field.key}><label htmlFor={field.key}>{field.label}</label><input id={field.key} type="number" step={field.step} value={form[field.key]} onChange={(event) => updateField(field.key, event.target.value)} required /></div>)}<button className="submit" disabled={loading}>{loading ? "Scoring borrower..." : "Run risk assessment"}</button></form>{error && <p className="error" role="alert">{error}</p>}</section>
      <section className="panel" aria-live="polite">{result ? <><div className="result-head"><div><div className="eyebrow">Assessment complete</div><h2>Default likelihood</h2></div><span className="band">{result.risk_band} risk</span></div><div className="probability"><strong>{(result.default_probability * 100).toFixed(1)}%</strong><span>Estimated probability of default</span></div><div className="chart-title">What influenced this score</div><ShapWaterfallChart attributions={result.attributions} /><div className="legend"><span><i style={{ background: "var(--red)" }} />increases risk</span><span><i style={{ background: "var(--green)" }} />reduces risk</span></div>{result.adverse_reasons.length > 0 && <div className="reasons"><h3>Primary adverse factors</h3><ul>{result.adverse_reasons.map((reason) => <li key={reason}>{reason}</li>)}</ul></div>}</> : <div className="empty"><div><div className="eyebrow">Awaiting profile</div><span>Enter borrower details to reveal the model explanation.</span></div></div>}</section>
    </div>
  </div></main>;
}