from typing import Any

from app.analytics.utils import cagr, extract_annual_values, pct, safe_div


def compute_growth_metrics(
    income_data: dict[str, Any],
    source: str,
) -> dict[str, Any]:
    annual = income_data.get("annual", [])
    revenue_series = extract_annual_values(annual, "Total Revenue")
    eps_series = extract_annual_values(annual, "Diluted EPS")
    if not eps_series:
        eps_series = extract_annual_values(annual, "Basic EPS")

    revenue_cagr_5y = None
    eps_cagr_5y = None

    if len(revenue_series) >= 2:
        years = min(5, len(revenue_series) - 1)
        start_rev = revenue_series[-(years + 1)][1]
        end_rev = revenue_series[-1][1]
        revenue_cagr_5y = cagr(start_rev, end_rev, years)

    if len(eps_series) >= 2:
        years = min(5, len(eps_series) - 1)
        start_eps = eps_series[-(years + 1)][1]
        end_eps = eps_series[-1][1]
        eps_cagr_5y = cagr(start_eps, end_eps, years)

    # YoY growth from last two annual periods
    revenue_yoy = None
    if len(revenue_series) >= 2:
        prev, curr = revenue_series[-2][1], revenue_series[-1][1]
        revenue_yoy = safe_div(curr - prev, abs(prev))

    return {
        "revenue_cagr_5y": {
            "value": revenue_cagr_5y,
            "display": pct(revenue_cagr_5y),
            "source": source,
        },
        "eps_cagr_5y": {
            "value": eps_cagr_5y,
            "display": pct(eps_cagr_5y),
            "source": source,
        },
        "revenue_yoy": {
            "value": revenue_yoy,
            "display": pct(revenue_yoy),
            "source": source,
        },
        "revenue_series": revenue_series,
        "eps_series": eps_series,
    }
