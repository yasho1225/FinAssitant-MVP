from typing import Any

import yfinance as yf
from tenacity import retry, stop_after_attempt, wait_exponential

from app.collectors.base import build_response, dataframe_to_records, normalize_ticker


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
def get_cash_flow(ticker: str) -> dict[str, Any]:
    symbol = normalize_ticker(ticker)
    stock = yf.Ticker(symbol)

    annual = stock.cashflow
    quarterly = stock.quarterly_cashflow

    return build_response(
        ticker=symbol,
        source="yfinance",
        data={
            "annual": dataframe_to_records(annual)[:5],
            "quarterly": dataframe_to_records(quarterly)[:8],
            "ttm": _compute_ttm_cashflow(quarterly),
        },
        metadata={"statement_type": "cash_flow"},
    )


def _compute_ttm_cashflow(quarterly_df) -> dict[str, float | None]:
    if quarterly_df is None or quarterly_df.empty:
        return {}
    fields = [
        "Operating Cash Flow",
        "Capital Expenditure",
        "Free Cash Flow",
    ]
    result: dict[str, float | None] = {}
    cols = list(quarterly_df.columns)[:4]
    for field in fields:
        if field in quarterly_df.index:
            values = [quarterly_df.loc[field, c] for c in cols]
            numeric = [float(v) for v in values if v == v]
            result[field] = sum(numeric) if numeric else None
        else:
            # Derive FCF if not present
            if field == "Free Cash Flow" and "Operating Cash Flow" in quarterly_df.index:
                ocf_vals = [quarterly_df.loc["Operating Cash Flow", c] for c in cols]
                capex_vals = [
                    quarterly_df.loc["Capital Expenditure", c]
                    for c in cols
                    if "Capital Expenditure" in quarterly_df.index
                ]
                if capex_vals:
                    ocf = sum(float(v) for v in ocf_vals if v == v)
                    capex = sum(float(v) for v in capex_vals if v == v)
                    result[field] = ocf + capex  # capex is typically negative
                else:
                    result[field] = None
            else:
                result[field] = None
    return result
