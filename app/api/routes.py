from fastapi import APIRouter, HTTPException

from app import __version__
from app.models.schemas import HealthResponse, ResearchRequest, ResearchResponse
from app.services.research_service import ResearchService

router = APIRouter()
_service = ResearchService()


@router.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok", version=__version__)


@router.post("/research", response_model=ResearchResponse)
def generate_research(request: ResearchRequest):
    """Generate a full investment memo for a US equity ticker."""
    try:
        return _service.run(request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Research failed: {exc}") from exc


@router.get("/analytics/{ticker}")
def get_analytics(ticker: str):
    """Return deterministic analytics only (no LLM)."""
    try:
        return _service.get_analytics_only(ticker)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
