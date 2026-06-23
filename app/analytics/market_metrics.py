import math
from typing import Any

import numpy as np
import yfinance as yf

from app.analytics.utils import pct, ratio, safe_div
from app.collectors.base import normalize_ticker


def compute_market_metrics(
    ticker: str,
    price_data: dict[str, Any],
    income_data: dict[str, Any],
    balance_data: dict[str, Any],
) -> dict[str, Any]:
    symbol = normalize_ticker(ticker)
    stock = yf.Ticker(symbol)
    info = stock.info or {}

    source = "yfinance"
    ttm = income_data.get("ttm", {})
    revenue = ttm.get("Total Revenue")
    net_income = ttm.get("Net Income")
    ebitda = ttm.get("EBITDA")

    market_cap = info.get("marketCap")
    enterprise_value = info.get("enterpriseValue")
    shares = info.get("sharesOutstanding")
    price = info.get("currentPrice") or info.get("regularMarketPrice")

    pe = info.get("trailingPE") or safe_div(market_cap, net_income)
    ps = safe_div(market_cap, revenue)
    ev_ebitda = safe_div(enterprise_value, ebitda)

    returns = _compute_returns(price_data.get("data", {}))
    volatility = _compute_volatility(price_data.get("data", {}).get("1y", []))
    max_drawdown = _compute_max_drawdown(price_data.get("data", {}).get("5y", []))

    return {
        "price": {"value": price, "display": f"${price:.2f}" if price else "N/A", "source": source},
        "market_cap": {"value": market_cap, "display": _fmt_large(market_cap), "source": source},
        "pe": {"value": pe, "display": ratio(pe), "source": source},
        "ev_ebitda": {"value": ev_ebitda, "display": ratio(ev_ebitda), "source": source},
        "ps": {"value": ps, "display": ratio(ps), "source": source},
        "return_1y": {"value": returns.get("1y"), "display": pct(returns.get("1y")), "source": source},
        "return_3y": {"value": returns.get("3y"), "display": pct(returns.get("3y")), "source": source},
        "return_5y": {"value": returns.get("5y"), "display": pct(returns.get("5y")), "source": source},
        "volatility_1y": {
            "value": volatility,
            "display": pct(volatility),
            "source": source,
        },
        "max_drawdown_5y": {
            "value": max_drawdown,
            "display": pct(max_drawdown),
            "source": source,
        },
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "company_name": info.get("longName") or info.get("shortName"),
        "business_summary": info.get("longBusinessSummary"),
    }


def _compute_returns(price_buckets: dict) -> dict[str, float | None]:
    result: dict[str, float | None] = {}
    for period in ("1y", "3y", "5y"):
        rows = price_buckets.get(period, [])
        if len(rows) < 2:
            result[period] = None
            continue
        start = rows[0]["close"]
        end = rows[-1]["close"]
        result[period] = safe_div(end - start, start)
    return result


def _compute_volatility(price_rows: list[dict]) -> float | None:
    if len(price_rows) < 20:
        return None
    closes = [r["close"] for r in price_rows]
    returns = np.diff(np.log(closes))
    return float(np.std(returns) * math.sqrt(252))


def _compute_max_drawdown(price_rows: list[dict]) -> float | None:
    if len(price_rows) < 2:
        return None
    closes = [r["close"] for r in price_rows]
    peak = closes[0]
    max_dd = 0.0
    for price in closes:
        if price > peak:
            peak = price
        dd = (price - peak) / peak
        if dd < max_dd:
            max_dd = dd
    return max_dd


def _fmt_large(value: float | None) -> str:
    if value is None:
        return "N/A"
    if value >= 1e12:
        return f"${value / 1e12:.2f}T"
    if value >= 1e9:
        return f"${value / 1e9:.2f}B"
    return f"${value:,.0f}"
