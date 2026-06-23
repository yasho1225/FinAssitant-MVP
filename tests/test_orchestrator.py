from unittest.mock import MagicMock, patch

import pytest

from app.orchestrator.llm import generate_offline_memo


def test_offline_memo_structure():
    analytics = {
        "ticker": "AAPL",
        "computed_at": "2025-01-01T00:00:00Z",
        "key_metrics_flat": {
            "revenue_cagr": "8.00%",
            "eps_cagr": "10.00%",
            "net_margin": "25.00%",
            "roic": "20.00%",
            "roe": "18.00%",
            "debt_equity": "1.50x",
        },
        "market": {
            "company_name": "Apple Inc.",
            "business_summary": "Technology company.",
            "pe": {"display": "28.00x"},
            "ev_ebitda": {"display": "22.00x"},
            "ps": {"display": "7.00x"},
        },
        "cash_flow": {"fcf_margin": {"display": "20.00%"}},
        "buffett_signals": {"signals_met": 3, "signals_total": 6},
        "peer_comparison": {"relative_valuation": {}},
    }
    news = {"source": "yfinance", "data": {"articles": []}}
    sec = {"data": {"filings": []}}

    memo, structured = generate_offline_memo("AAPL", analytics, news, sec)

    assert structured.ticker == "AAPL"
    assert structured.recommendation.value in ("BUY", "HOLD", "SELL")
    assert 0 <= structured.confidence <= 1
    assert memo.executive_summary
    assert memo.data_appendix
    assert structured.key_metrics.revenue_cagr == "8.00%"
