from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Recommendation(str, Enum):
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"


class ResearchRequest(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=10, description="US equity ticker symbol")
    news_window_days: int = Field(default=60, ge=7, le=90)
    include_peers: bool = True


class MetricValue(BaseModel):
    value: float | None
    unit: str = ""
    period: str | None = None
    source: str
    as_of: datetime


class CitedMetric(BaseModel):
    name: str
    value: str
    source: str
    as_of: datetime


class KeyMetrics(BaseModel):
    revenue_cagr: str
    eps_cagr: str
    net_margin: str
    roic: str
    roe: str
    debt_equity: str


class ThesisPoints(BaseModel):
    bull: list[str]
    bear: list[str]


class MemoStructuredOutput(BaseModel):
    ticker: str
    recommendation: Recommendation
    confidence: float = Field(..., ge=0.0, le=1.0)
    key_metrics: KeyMetrics
    thesis: ThesisPoints
    risks: list[str]
    catalysts: list[str]
    mind_change_triggers: list[str]


class InvestmentMemo(BaseModel):
    executive_summary: str
    business_overview: str
    financial_health: str
    valuation: str
    catalysts: str
    risks: str
    bear_case: str
    what_would_change_my_mind: str
    data_appendix: str
    citations: list[str]


class ResearchResponse(BaseModel):
    ticker: str
    generated_at: datetime
    memo: InvestmentMemo
    structured: MemoStructuredOutput
    analytics_snapshot: dict[str, Any]
    raw_sources: dict[str, str]


class HealthResponse(BaseModel):
    status: str
    version: str
