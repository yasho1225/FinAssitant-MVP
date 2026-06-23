from typing import Any

from app.analytics.utils import pct, safe_div


def compute_profitability_metrics(
    income_data: dict[str, Any],
    source: str,
) -> dict[str, Any]:
    ttm = income_data.get("ttm", {})
    revenue = ttm.get("Total Revenue")
    gross_profit = ttm.get("Gross Profit")
    operating_income = ttm.get("Operating Income")
    net_income = ttm.get("Net Income")

    gross_margin = safe_div(gross_profit, revenue)
    operating_margin = safe_div(operating_income, revenue)
    net_margin = safe_div(net_income, revenue)

    # Annual margin trends
    annual = income_data.get("annual", [])
    margin_trend = []
    for record in annual[:5]:
        rev = record.get("Total Revenue")
        ni = record.get("Net Income")
        margin_trend.append(
            {
                "period": record.get("period"),
                "net_margin": safe_div(ni, rev),
            }
        )

    return {
        "gross_margin": {"value": gross_margin, "display": pct(gross_margin), "source": source},
        "operating_margin": {
            "value": operating_margin,
            "display": pct(operating_margin),
            "source": source,
        },
        "net_margin": {"value": net_margin, "display": pct(net_margin), "source": source},
        "net_margin_trend": margin_trend,
    }
