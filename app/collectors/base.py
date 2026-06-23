from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_ticker(ticker: str) -> str:
    return ticker.strip().upper()


def dataframe_to_records(df) -> list[dict[str, Any]]:
    if df is None or df.empty:
        return []
    records: list[dict[str, Any]] = []
    for col in df.columns:
        period = str(col)
        row_data: dict[str, Any] = {"period": period}
        for idx, val in df[col].items():
            key = str(idx)
            if val is None or (isinstance(val, float) and val != val):
                row_data[key] = None
            else:
                row_data[key] = float(val) if isinstance(val, (int, float)) else val
        records.append(row_data)
    return records


def build_response(
    *,
    ticker: str,
    source: str,
    data: Any,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "ticker": normalize_ticker(ticker),
        "source": source,
        "fetched_at": utc_now_iso(),
        "metadata": metadata or {},
        "data": data,
    }
