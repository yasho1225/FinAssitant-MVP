from typing import Any


def safe_div(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator is None or denominator == 0:
        return None
    return numerator / denominator


def cagr(start: float | None, end: float | None, years: float) -> float | None:
    if start is None or end is None or start <= 0 or end <= 0 or years <= 0:
        return None
    return (end / start) ** (1 / years) - 1


def pct(value: float | None, decimals: int = 2) -> str:
    if value is None:
        return "N/A"
    return f"{value * 100:.{decimals}f}%"


def ratio(value: float | None, decimals: int = 2) -> str:
    if value is None:
        return "N/A"
    return f"{value:.{decimals}f}x"


def money(value: float | None) -> str:
    if value is None:
        return "N/A"
    abs_val = abs(value)
    if abs_val >= 1e12:
        return f"${value / 1e12:.2f}T"
    if abs_val >= 1e9:
        return f"${value / 1e9:.2f}B"
    if abs_val >= 1e6:
        return f"${value / 1e6:.2f}M"
    return f"${value:,.0f}"


def extract_annual_values(annual_records: list[dict], field: str) -> list[tuple[str, float]]:
    """Extract field values from annual statement records, sorted oldest to newest."""
    values: list[tuple[str, float]] = []
    for record in annual_records:
        period = record.get("period", "")
        val = record.get(field)
        if val is not None:
            values.append((period, float(val)))
    # yfinance periods are typically newest first in records
    values.reverse()
    return values
