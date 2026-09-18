# Credit Risk Explainability Engine

FastAPI and Next.js application for producing a credit default probability with SHAP-based feature explanations.

## Run locally

Start the API:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
uvicorn app.main:app --app-dir backend --reload --port 8000
```

Start the dashboard in a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

The dashboard uses `http://localhost:8000` by default. Set `NEXT_PUBLIC_API_URL` to point it at another API origin. The model adapter trains a deterministic fallback classifier when no persisted Joblib model exists; replace that adapter's model path for a production-trained model.