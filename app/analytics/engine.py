"""Layer B — pure deterministic analytics engine."""

from datetime import datetime, timezone
from typing import Any

import yfinance as yf

from app.analytics.balance_sheet_metrics import compute_balance_sheet_metrics
from app.analytics.capital_efficiency import compute_capital_efficiency
from app.analytics.cash_flow_metrics import compute_cash_flow_metrics
from app.analytics.growth import compute_growth_metrics
from app.analytics.market_metrics import compute_market_metrics
from app.analytics.profitability import compute_profitability_metrics
from app.collectors.base import normalize_ticker


def compute_buffett_signals(metrics: dict[str, Any]) -> dict[str, Any]:
    """Soft screening signals — classification only, NOT filters."""
    checks = {
        "revenue_cagr_above_10pct": _signal(
            metrics["growth"]["revenue_cagr_5y"]["value"], 0.10, ">"
        ),
        "eps_cagr_above_10pct": _signal(metrics["growth"]["eps_cagr_5y"]["value"], 0.10, ">"),
        "net_margin_above_10pct": _signal(
            metrics["profitability"]["net_margin"]["value"], 0.10, ">"
        ),
        "roic_above_15pct": _signal(
            metrics["capital_efficiency"]["roic"]["value"], 0.15, ">"
        ),
        "roe_above_15pct": _signal(metrics["capital_efficiency"]["roe"]["value"], 0.15, ">"),
        "debt_equity_below_0_5": _signal(
            metrics["balance_sheet"]["debt_equity"]["value"], 0.5, "<"
        ),
    }
    met = sum(1 for v in checks.values() if v["met"] is True)
    total = sum(1 for v in checks.values() if v["met"] is not None)
    return {
        "signals": checks,
        "signals_met": met,
        "signals_total": total,
        "note": "Soft screening signals for narrative context only — not used as filters.",
    }


def _signal(value: float | None, threshold: float, op: str) -> dict[str, Any]:
    if value is None:
        return {"met": None, "threshold": threshold, "value": None}
    if op == ">":
        met = value > threshold
    else:
        met = value < threshold
    return {"met": met, "threshold": threshold, "value": value}


def compute_peer_comparison(
    ticker: str,
    peers_data: dict[str, Any],
    subject_metrics: dict[str, Any],
) -> dict[str, Any]:
    """Compute peer median metrics for relative valuation context."""
    peer_tickers = peers_data.get("data", {}).get("peers", [])[:4]
    peer_snapshots: list[dict[str, Any]] = []

    compare_keys = ["pe", "ev_ebitda", "ps", "net_margin", "roe", "roic"]

    for peer in peer_tickers:
        try:
            stock = yf.Ticker(peer)
            info = stock.info or {}
            fin = stock.financials
            rev = None
            ni = None
            if fin is not None and not fin.empty:
                if "Total Revenue" in fin.index:
                    rev = float(fin.loc["Total Revenue"].iloc[0])
                if "Net Income" in fin.index:
                    ni = float(fin.loc["Net Income"].iloc[0])
            peer_snapshots.append(
                {
                    "ticker": peer,
                    "pe": info.get("trailingPE"),
                    "ev_ebitda": safe_div(info.get("enterpriseValue"), info.get("ebitda")),
                    "ps": safe_div(info.get("marketCap"), rev),
                    "net_margin": safe_div(ni, rev),
                    "roe": info.get("returnOnEquity"),
                    "roic": None,
                }
            )
        except Exception:
            continue

    medians: dict[str, float | None] = {}
    for key in compare_keys:
        vals = [p[key] for p in peer_snapshots if p.get(key) is not None]
        medians[key] = _median(vals) if vals else None

    subject_market = subject_metrics.get("market", {})
    relative: dict[str, Any] = {}
    for key in compare_keys:
        subj_val = subject_market.get(key, {}).get("value")
        if key in ("net_margin", "roe", "roic"):
            subj_val = subject_metrics.get(
                "profitability" if key == "net_margin" else "capital_efficiency", {}
            ).get(key, {}).get("value")
        peer_med = medians.get(key)
        relative[key] = {
            "subject": subj_val,
            "peer_median": peer_med,
            "vs_peers": _compare(subj_val, peer_med),
        }

    return {
        "peer_tickers": [p["ticker"] for p in peer_snapshots],
        "peer_snapshots": peer_snapshots,
        "peer_medians": medians,
        "relative_valuation": relative,
        "source": peers_data.get("source", "yfinance"),
    }


def safe_div(a, b):
    if a is None or b is None or b == 0:
        return None
    return a / b


def _median(vals: list[float]) -> float:
    s = sorted(vals)
    n = len(s)
    mid = n // 2
    if n % 2:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2


def _compare(subject: float | None, peer: float | None) -> str:
    if subject is None or peer is None:
        return "insufficient_data"
    if subject > peer * 1.1:
        return "above_peers"
    if subject < peer * 0.9:
        return "below_peers"
    return "in_line"


class AnalyticsEngine:
    """Orchestrates all deterministic metric computation."""

    def run(
        self,
        ticker: str,
        *,
        price_data: dict,
        income_data: dict,
        balance_data: dict,
        cashflow_data: dict,
        peers_data: dict,
    ) -> dict[str, Any]:
        symbol = normalize_ticker(ticker)
        income_payload = income_data.get("data", {})
        balance_payload = balance_data.get("data", {})
        cashflow_payload = cashflow_data.get("data", {})

        growth = compute_growth_metrics(income_payload, income_data.get("source", "yfinance"))
        profitability = compute_profitability_metrics(
            income_payload, income_data.get("source", "yfinance")
        )
        capital_efficiency = compute_capital_efficiency(
            income_payload, balance_payload, income_data.get("source", "yfinance")
        )
        cash_flow = compute_cash_flow_metrics(
            income_payload, cashflow_payload, cashflow_data.get("source", "yfinance")
        )
        balance_sheet = compute_balance_sheet_metrics(
            income_payload, balance_payload, balance_data.get("source", "yfinance")
        )
        market = compute_market_metrics(symbol, price_data, income_payload, balance_payload)

        metrics = {
            "ticker": symbol,
            "computed_at": datetime.now(timezone.utc).isoformat(),
            "growth": growth,
            "profitability": profitability,
            "capital_efficiency": capital_efficiency,
            "cash_flow": cash_flow,
            "balance_sheet": balance_sheet,
            "market": market,
        }

        metrics["buffett_signals"] = compute_buffett_signals(metrics)
        metrics["peer_comparison"] = compute_peer_comparison(symbol, peers_data, metrics)

        metrics["key_metrics_flat"] = {
            "revenue_cagr": growth["revenue_cagr_5y"]["display"],
            "eps_cagr": growth["eps_cagr_5y"]["display"],
            "net_margin": profitability["net_margin"]["display"],
            "roic": capital_efficiency["roic"]["display"],
            "roe": capital_efficiency["roe"]["display"],
            "debt_equity": balance_sheet["debt_equity"]["display"],
        }

        return metrics
