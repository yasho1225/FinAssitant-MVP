from typing import Any

from app.analytics.utils import money, pct, safe_div


def compute_cash_flow_metrics(
    income_data: dict[str, Any],
    cashflow_data: dict[str, Any],
    source: str,
) -> dict[str, Any]:
    ttm_income = income_data.get("ttm", {})
    ttm_cf = cashflow_data.get("ttm", {})
    revenue = ttm_income.get("Total Revenue")
    net_income = ttm_income.get("Net Income")
    ocf = ttm_cf.get("Operating Cash Flow")
    fcf = ttm_cf.get("Free Cash Flow")

    if fcf is None and ocf is not None:
        capex = ttm_cf.get("Capital Expenditure")
        if capex is not None:
            fcf = ocf + capex  # capex negative

    fcf_margin = safe_div(fcf, revenue)
    fcf_conversion = safe_div(fcf, net_income)

    return {
        "free_cash_flow": {"value": fcf, "display": money(fcf), "source": source},
        "fcf_margin": {"value": fcf_margin, "display": pct(fcf_margin), "source": source},
        "fcf_conversion_ratio": {
            "value": fcf_conversion,
            "display": pct(fcf_conversion),
            "source": source,
        },
        "operating_cash_flow": {"value": ocf, "display": money(ocf), "source": source},
    }
