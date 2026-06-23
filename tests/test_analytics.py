import pytest

from app.analytics.engine import AnalyticsEngine, compute_buffett_signals, safe_div
from app.analytics.growth import compute_growth_metrics
from app.analytics.utils import cagr, pct


def test_cagr_basic():
    result = cagr(100, 161, 5)
    assert result is not None
    assert abs(result - 0.10) < 0.01


def test_cagr_invalid():
    assert cagr(None, 100, 5) is None
    assert cagr(100, None, 5) is None
    assert cagr(-100, 100, 5) is None


def test_safe_div():
    assert safe_div(10, 2) == 5
    assert safe_div(10, 0) is None
    assert safe_div(None, 2) is None


def test_pct_format():
    assert pct(0.1234) == "12.34%"
    assert pct(None) == "N/A"


def test_growth_metrics_empty():
    result = compute_growth_metrics({"annual": [], "ttm": {}}, "test")
    assert result["revenue_cagr_5y"]["value"] is None


def test_buffett_signals():
    metrics = {
        "growth": {
            "revenue_cagr_5y": {"value": 0.15},
            "eps_cagr_5y": {"value": 0.12},
        },
        "profitability": {"net_margin": {"value": 0.11}},
        "capital_efficiency": {"roic": {"value": 0.18}, "roe": {"value": 0.20}},
        "balance_sheet": {"debt_equity": {"value": 0.3}},
    }
    signals = compute_buffett_signals(metrics)
    assert signals["signals_met"] >= 4
    assert "note" in signals


def test_analytics_engine_integration():
    """Integration test using mocked minimal data structures."""
    engine = AnalyticsEngine()
    income = {
        "source": "test",
        "data": {
            "annual": [
                {
                    "period": "2024",
                    "Total Revenue": 1000,
                    "Net Income": 100,
                    "Gross Profit": 400,
                    "Operating Income": 200,
                    "Diluted EPS": 5.0,
                },
                {
                    "period": "2020",
                    "Total Revenue": 600,
                    "Net Income": 50,
                    "Diluted EPS": 2.5,
                },
            ],
            "ttm": {
                "Total Revenue": 1000,
                "Net Income": 100,
                "Gross Profit": 400,
                "Operating Income": 200,
                "EBITDA": 250,
            },
        },
    }
    balance = {
        "source": "test",
        "data": {
            "latest": {
                "Stockholders Equity": 500,
                "Total Debt": 100,
                "Cash And Cash Equivalents": 50,
                "Total Assets": 800,
                "Current Assets": 300,
                "Current Liabilities": 150,
            }
        },
    }
    cashflow = {
        "source": "test",
        "data": {"ttm": {"Operating Cash Flow": 150, "Free Cash Flow": 120}},
    }
    price = {
        "source": "test",
        "data": {
            "1y": [{"close": 100}, {"close": 110}],
            "3y": [{"close": 80}, {"close": 110}],
            "5y": [{"close": 60}, {"close": 50}, {"close": 110}],
        },
    }
    peers = {"source": "test", "data": {"peers": []}}

    result = engine.run(
        "TEST",
        price_data=price,
        income_data=income,
        balance_data=balance,
        cashflow_data=cashflow,
        peers_data=peers,
    )

    assert result["ticker"] == "TEST"
    assert result["profitability"]["net_margin"]["display"] == "10.00%"
    assert "key_metrics_flat" in result
    assert result["buffett_signals"]["signals_total"] >= 1
