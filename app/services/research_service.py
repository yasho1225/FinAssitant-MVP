from datetime import datetime, timezone
from typing import Any

from app.analytics import AnalyticsEngine
from app.collectors import (
    get_balance_sheet,
    get_cash_flow,
    get_income_statement,
    get_news,
    get_peers,
    get_price_history,
    get_sec_filings,
)
from app.config import get_settings
from app.models.database import ResearchRun, get_session_factory
from app.models.schemas import ResearchRequest, ResearchResponse
from app.orchestrator.llm import LLMOrchestrator, generate_offline_memo


class ResearchService:
    """End-to-end pipeline: collect → analyze → synthesize."""

    def __init__(self) -> None:
        self.analytics_engine = AnalyticsEngine()

    def run(self, request: ResearchRequest) -> ResearchResponse:
        ticker = request.ticker.strip().upper()

        # Layer A — Data Collection
        price_data = get_price_history(ticker)
        income_data = get_income_statement(ticker)
        balance_data = get_balance_sheet(ticker)
        cashflow_data = get_cash_flow(ticker)
        sec_data = get_sec_filings(ticker)
        news_data = get_news(ticker, window=request.news_window_days)
        peers_data = get_peers(ticker) if request.include_peers else {
            "data": {"peers": []},
            "source": "none",
        }

        # Layer B — Analytics
        analytics = self.analytics_engine.run(
            ticker,
            price_data=price_data,
            income_data=income_data,
            balance_data=balance_data,
            cashflow_data=cashflow_data,
            peers_data=peers_data,
        )

        # Layer C — LLM Narrative
        settings = get_settings()
        if settings.openai_api_key:
            orchestrator = LLMOrchestrator()
            memo, structured = orchestrator.generate_memo(
                ticker, analytics, news_data, sec_data
            )
        else:
            memo, structured = generate_offline_memo(
                ticker, analytics, news_data, sec_data
            )

        response = ResearchResponse(
            ticker=ticker,
            generated_at=datetime.now(timezone.utc),
            memo=memo,
            structured=structured,
            analytics_snapshot=analytics,
            raw_sources={
                "price": price_data.get("source", ""),
                "income": income_data.get("source", ""),
                "balance_sheet": balance_data.get("source", ""),
                "cash_flow": cashflow_data.get("source", ""),
                "sec": sec_data.get("source", ""),
                "news": news_data.get("source", ""),
                "peers": peers_data.get("source", ""),
            },
        )

        self._persist(ticker, response)
        return response

    def _persist(self, ticker: str, response: ResearchResponse) -> None:
        factory = get_session_factory()
        if factory is None:
            return
        session = factory()
        try:
            run = ResearchRun(
                ticker=ticker,
                recommendation=response.structured.recommendation.value,
                confidence=response.structured.confidence,
                memo_json=response.memo.model_dump(),
                structured_json=response.structured.model_dump(),
                analytics_json=response.analytics_snapshot,
            )
            session.add(run)
            session.commit()
        except Exception:
            session.rollback()
        finally:
            session.close()

    def get_analytics_only(self, ticker: str) -> dict[str, Any]:
        """Expose analytics without LLM — useful for debugging."""
        ticker = ticker.strip().upper()
        price_data = get_price_history(ticker)
        income_data = get_income_statement(ticker)
        balance_data = get_balance_sheet(ticker)
        cashflow_data = get_cash_flow(ticker)
        peers_data = get_peers(ticker)
        return self.analytics_engine.run(
            ticker,
            price_data=price_data,
            income_data=income_data,
            balance_data=balance_data,
            cashflow_data=cashflow_data,
            peers_data=peers_data,
        )
