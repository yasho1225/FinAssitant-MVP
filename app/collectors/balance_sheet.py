from typing import Any

import yfinance as yf
from tenacity import retry, stop_after_attempt, wait_exponential

from app.collectors.base import build_response, dataframe_to_records, normalize_ticker


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
def get_balance_sheet(ticker: str) -> dict[str, Any]:
    symbol = normalize_ticker(ticker)
    stock = yf.Ticker(symbol)

    annual = stock.balance_sheet
    quarterly = stock.quarterly_balance_sheet

    latest_df = quarterly if quarterly is not None and not quarterly.empty else annual

    return build_response(
        ticker=symbol,
        source="yfinance",
        data={
            "annual": dataframe_to_records(annual)[:5],
            "quarterly": dataframe_to_records(quarterly)[:8],
            "latest": _latest_period(latest_df),
        },
        metadata={"statement_type": "balance_sheet"},
    )


def _latest_period(df) -> dict[str, float | None]:
    if df is None or df.empty:
        return {}
    col = df.columns[0]
    fields = [
        "Total Assets",
        "Total Liabilities Net Minority Interest",
        "Total Debt",
        "Net Debt",
        "Stockholders Equity",
        "Cash And Cash Equivalents",
        "Current Assets",
        "Current Liabilities",
    ]
    result: dict[str, float | None] = {}
    for field in fields:
        if field in df.index:
            val = df.loc[field, col]
            result[field] = float(val) if val == val else None
        else:
            result[field] = None
    return result
