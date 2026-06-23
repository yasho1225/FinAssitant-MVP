from typing import Any

import yfinance as yf
from tenacity import retry, stop_after_attempt, wait_exponential

from app.collectors.base import build_response, normalize_ticker


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
def get_price_history(ticker: str) -> dict[str, Any]:
    """Fetch 1Y, 3Y, 5Y daily price history."""
    symbol = normalize_ticker(ticker)
    stock = yf.Ticker(symbol)
    hist_5y = stock.history(period="5y", auto_adjust=True)
    if hist_5y.empty:
        raise ValueError(f"No price history for {symbol}")

    def serialize(df):
        rows = []
        for idx, row in df.iterrows():
            rows.append(
                {
                    "date": idx.strftime("%Y-%m-%d"),
                    "open": float(row["Open"]),
                    "high": float(row["High"]),
                    "low": float(row["Low"]),
                    "close": float(row["Close"]),
                    "volume": int(row["Volume"]),
                }
            )
        return rows

    dates = hist_5y.index
    one_year_ago = dates[-1] - __import__("pandas").DateOffset(years=1)
    three_year_ago = dates[-1] - __import__("pandas").DateOffset(years=3)

    hist_1y = hist_5y[hist_5y.index >= one_year_ago]
    hist_3y = hist_5y[hist_5y.index >= three_year_ago]

    info = stock.info or {}
    return build_response(
        ticker=symbol,
        source="yfinance",
        data={
            "1y": serialize(hist_1y),
            "3y": serialize(hist_3y),
            "5y": serialize(hist_5y),
            "currency": info.get("currency", "USD"),
            "exchange": info.get("exchange"),
        },
        metadata={"periods": ["1y", "3y", "5y"], "interval": "1d"},
    )
