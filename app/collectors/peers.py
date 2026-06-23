from typing import Any

import yfinance as yf
from tenacity import retry, stop_after_attempt, wait_exponential

from app.collectors.base import build_response, normalize_ticker

# Sector-based peer mapping for common US sectors (MVP fallback)
SECTOR_PEERS: dict[str, list[str]] = {
    "Technology": ["MSFT", "GOOGL", "META", "ORCL", "CRM"],
    "Consumer Cyclical": ["AMZN", "HD", "NKE", "SBUX", "TJX"],
    "Consumer Defensive": ["PG", "KO", "PEP", "WMT", "COST"],
    "Healthcare": ["JNJ", "UNH", "PFE", "ABBV", "MRK"],
    "Financial Services": ["JPM", "BAC", "WFC", "GS", "MS"],
    "Industrials": ["CAT", "GE", "HON", "UPS", "BA"],
    "Energy": ["XOM", "CVX", "COP", "SLB", "EOG"],
    "Communication Services": ["DIS", "NFLX", "CMCSA", "T", "VZ"],
    "Utilities": ["NEE", "DUK", "SO", "D", "AEP"],
    "Real Estate": ["AMT", "PLD", "EQIX", "SPG", "O"],
    "Basic Materials": ["LIN", "APD", "SHW", "ECL", "NEM"],
}


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
def get_peers(ticker: str) -> dict[str, Any]:
    """Resolve sector-based peer tickers, excluding the subject ticker."""
    symbol = normalize_ticker(ticker)
    stock = yf.Ticker(symbol)
    info = stock.info or {}

    sector = info.get("sector") or "Technology"
    industry = info.get("industry")
    recommended = info.get("recommendedSymbols") or []

    peers: list[str] = []
    if recommended:
        peers = [p.get("symbol") for p in recommended if isinstance(p, dict) and p.get("symbol")]
        peers = [p for p in peers if p and p.upper() != symbol][:8]

    if not peers:
        sector_list = SECTOR_PEERS.get(sector, SECTOR_PEERS["Technology"])
        peers = [p for p in sector_list if p != symbol][:5]

    return build_response(
        ticker=symbol,
        source="yfinance+sector_map",
        data={
            "sector": sector,
            "industry": industry,
            "peers": peers,
        },
        metadata={"mapping": "sector_based"},
    )
