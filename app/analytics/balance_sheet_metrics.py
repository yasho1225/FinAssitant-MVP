from typing import Any

from app.analytics.utils import pct, ratio, safe_div


def compute_balance_sheet_metrics(
    income_data: dict[str, Any],
    balance_data: dict[str, Any],
    source: str,
) -> dict[str, Any]:
    latest = balance_data.get("latest", {})
    ttm = income_data.get("ttm", {})

    equity = latest.get("Stockholders Equity")
    total_debt = latest.get("Total Debt")
    net_debt = latest.get("Net Debt")
    cash = latest.get("Cash And Cash Equivalents")
    ebitda = ttm.get("EBITDA")
    interest_expense = None

    # Try to get interest from annual
    for record in income_data.get("annual", [])[:1]:
        interest_expense = record.get("Interest Expense")

    if total_debt is None and equity is not None:
        total_debt = 0

    if net_debt is None and total_debt is not None and cash is not None:
        net_debt = total_debt - cash

    debt_equity = safe_div(total_debt, equity)
    net_debt_ebitda = safe_div(net_debt, ebitda)

    # Interest coverage = EBIT / Interest
    operating_income = ttm.get("Operating Income")
    interest_coverage = None
    if interest_expense and interest_expense != 0:
        interest_coverage = safe_div(operating_income, abs(interest_expense))

    current_assets = latest.get("Current Assets")
    current_liabilities = latest.get("Current Liabilities")
    current_ratio = safe_div(current_assets, current_liabilities)

    return {
        "debt_equity": {"value": debt_equity, "display": ratio(debt_equity), "source": source},
        "net_debt_ebitda": {
            "value": net_debt_ebitda,
            "display": ratio(net_debt_ebitda),
            "source": source,
        },
        "interest_coverage": {
            "value": interest_coverage,
            "display": ratio(interest_coverage),
            "source": source,
        },
        "current_ratio": {
            "value": current_ratio,
            "display": ratio(current_ratio),
            "source": source,
        },
    }
