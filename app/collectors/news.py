from datetime import datetime, timedelta, timezone
from typing import Any

import httpx
import yfinance as yf
from tenacity import retry, stop_after_attempt, wait_exponential

from app.collectors.base import build_response, normalize_ticker
from app.config import get_settings


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
def get_news(ticker: str, window: int = 60) -> dict[str, Any]:
    """Fetch news for ticker within window (days). Uses NewsAPI if configured, else yfinance."""
    symbol = normalize_ticker(ticker)
    settings = get_settings()
    cutoff = datetime.now(timezone.utc) - timedelta(days=window)

    articles: list[dict[str, Any]] = []
    source = "yfinance"

    if settings.news_api_key:
        articles = _fetch_newsapi(symbol, window, settings.news_api_key)
        source = "newsapi"

    if not articles:
        articles = _fetch_yfinance_news(symbol, cutoff)
        source = "yfinance"

    return build_response(
        ticker=symbol,
        source=source,
        data={"articles": articles, "window_days": window},
        metadata={"count": len(articles)},
    )


def _fetch_yfinance_news(symbol: str, cutoff: datetime) -> list[dict[str, Any]]:
    stock = yf.Ticker(symbol)
    raw = stock.news or []
    articles = []
    for item in raw:
        pub = item.get("providerPublishTime") or item.get("pubDate")
        published = None
        if pub:
            if isinstance(pub, (int, float)):
                published = datetime.fromtimestamp(pub, tz=timezone.utc)
            else:
                try:
                    published = datetime.fromisoformat(str(pub).replace("Z", "+00:00"))
                except ValueError:
                    published = None
        if published and published < cutoff:
            continue
        articles.append(
            {
                "title": item.get("title", ""),
                "publisher": item.get("publisher", item.get("source", "")),
                "link": item.get("link", item.get("url", "")),
                "published_at": published.isoformat() if published else None,
                "summary": item.get("summary", ""),
            }
        )
    return articles[:30]


def _fetch_newsapi(symbol: str, window: int, api_key: str) -> list[dict[str, Any]]:
    from_date = (datetime.now(timezone.utc) - timedelta(days=window)).strftime("%Y-%m-%d")
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": symbol,
        "from": from_date,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 30,
        "apiKey": api_key,
    }
    with httpx.Client(timeout=20.0) as client:
        resp = client.get(url, params=params)
        if resp.status_code != 200:
            return []
        data = resp.json()
    articles = []
    for item in data.get("articles", []):
        articles.append(
            {
                "title": item.get("title", ""),
                "publisher": (item.get("source") or {}).get("name", ""),
                "link": item.get("url", ""),
                "published_at": item.get("publishedAt"),
                "summary": item.get("description", ""),
            }
        )
    return articles
