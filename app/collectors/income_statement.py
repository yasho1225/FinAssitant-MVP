from typing import Any

import yfinance as yf
from tenacity import retry, stop_after_attempt, wait_exponential

from app.collectors.base import build_response, dataframe_to_records, normalize_ticker


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
def get_income_statement(ticker: str) -> dict[str, Any]:
    """Fetch quarterly + annual income statements (up to 5Y annual, 8Q quarterly)."""
    symbol = normalize_ticker(ticker)
    stock = yf.Ticker(symbol)

    annual = stock.financials
    quarterly = stock.quarterly_financials

    annual_records = dataframe_to_records(annual)
    quarterly_records = dataframe_to_records(quarterly)

    # TTM approximation from last 4 quarters
    ttm = _compute_ttm(quarterly)

    return build_response(
        ticker=symbol,
        source="yfinance",
        data={
            "annual": annual_records[:5],
            "quarterly": quarterly_records[:8],
            "ttm": ttm,
        },
        metadata={"statement_type": "income", "quarters": min(8, len(quarterly_records))},
    )


def _compute_ttm(quarterly_df) -> dict[str, float | None]:
    if quarterly_df is None or quarterly_df.empty:
        return {}

    ttm_fields = [
        "Total Revenue",
        "Gross Profit",
        "Operating Income",
        "Net Income",
        "EBITDA",
        "Basic EPS",
        "Diluted EPS",
    ]
    result: dict[str, float | None] = {}
    cols = list(quarterly_df.columns)[:4]
    for field in ttm_fields:
        if field in quarterly_df.index:
            values = [quarterly_df.loc[field, c] for c in cols]
            numeric = [float(v) for v in values if v == v]
            result[field] = sum(numeric) if numeric else None
        else:
            result[field] = None
    return result
