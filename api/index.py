"""Vercel serverless entrypoint for the FastAPI application."""

import sys
from pathlib import Path

from mangum import Mangum

# The backend package uses ``app.*`` imports, so expose backend as a package root.
BACKEND_DIR = Path(__file__).resolve().parent.parent / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.main import app as fastapi_app

app = fastapi_app
handler = Mangum(app)