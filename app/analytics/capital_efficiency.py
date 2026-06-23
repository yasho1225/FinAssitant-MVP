from typing import Any

from app.analytics.utils import pct, safe_div


def compute_capital_efficiency(
    income_data: dict[str, Any],
    balance_data: dict[str, Any],
    source: str,
) -> dict[str, Any]:
    ttm = income_data.get("ttm", {})
    latest = balance_data.get("latest", {})
    net_income = ttm.get("Net Income")
    equity = latest.get("Stockholders Equity")
    total_debt = latest.get("Total Debt") or 0
    cash = latest.get("Cash And Cash Equivalents") or 0
    total_assets = latest.get("Total Assets")

    roe = safe_div(net_income, equity)

    # ROIC = NOPAT / Invested Capital
    # NOPAT ≈ Operating Income * (1 - effective tax rate)
    operating_income = ttm.get("Operating Income")
    tax_rate = None
    tax_provision = None
    pretax = ttm.get("Pretax Income")
    if pretax and net_income is not None:
        tax_provision = pretax - net_income if pretax else None
        tax_rate = safe_div(tax_provision, pretax) if pretax else 0.21

    effective_tax = tax_rate if tax_rate is not None else 0.21
    nopat = operating_income * (1 - effective_tax) if operating_income is not None else None
    invested_capital = None
    if equity is not None:
        invested_capital = equity + (total_debt or 0) - (cash or 0)
    roic = safe_div(nopat, invested_capital)

    return {
        "roe": {"value": roe, "display": pct(roe), "source": source},
        "roic": {"value": roic, "display": pct(roic), "source": source},
        "invested_capital": invested_capital,
        "nopat": nopat,
    }
