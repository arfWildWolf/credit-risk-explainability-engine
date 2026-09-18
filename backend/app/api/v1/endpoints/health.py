"""Health endpoint."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    """Confirm the API process is accepting requests."""

    return {"status": "ok"}