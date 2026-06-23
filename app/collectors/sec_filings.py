from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from app.collectors.base import build_response, normalize_ticker
from app.config import get_settings


SEC_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SEC_SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
def get_sec_filings(ticker: str) -> dict[str, Any]:
    """Fetch recent 10-K, 10-Q, and 8-K filings from SEC EDGAR."""
    symbol = normalize_ticker(ticker)
    settings = get_settings()
    headers = {"User-Agent": settings.sec_user_agent, "Accept": "application/json"}

    cik = _resolve_cik(symbol, headers)
    if not cik:
        return build_response(
            ticker=symbol,
            source="sec_edgar",
            data={"filings": [], "cik": None},
            metadata={"error": f"CIK not found for {symbol}"},
        )

    url = SEC_SUBMISSIONS_URL.format(cik=cik.zfill(10))
    with httpx.Client(timeout=30.0, headers=headers) as client:
        resp = client.get(url)
        resp.raise_for_status()
        payload = resp.json()

    recent = payload.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    accessions = recent.get("accessionNumber", [])
    primary_docs = recent.get("primaryDocument", [])

    target_forms = {"10-K", "10-Q", "8-K"}
    filings = []
    for i, form in enumerate(forms):
        if form not in target_forms:
            continue
        accession = accessions[i].replace("-", "")
        doc = primary_docs[i] if i < len(primary_docs) else ""
        filing_url = (
            f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession}/{doc}"
            if doc
            else f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type={form}"
        )
        filings.append(
            {
                "form": form,
                "filing_date": dates[i],
                "accession_number": accessions[i],
                "url": filing_url,
            }
        )
        if len([f for f in filings if f["form"] == "10-K"]) >= 2 and len(filings) >= 15:
            break

    # Ensure at least one 10-K
    ten_k = [f for f in filings if f["form"] == "10-K"]
    company_name = payload.get("name", "")

    return build_response(
        ticker=symbol,
        source="sec_edgar",
        data={
            "cik": cik,
            "company_name": company_name,
            "filings": filings[:20],
            "has_10k": len(ten_k) > 0,
        },
        metadata={"forms": list(target_forms)},
    )


_cik_cache: dict[str, str] | None = None


def _resolve_cik(ticker: str, headers: dict[str, str]) -> str | None:
    global _cik_cache
    if _cik_cache is None:
        with httpx.Client(timeout=30.0, headers=headers) as client:
            resp = client.get(SEC_TICKERS_URL)
            resp.raise_for_status()
            raw = resp.json()
        _cik_cache = {}
        for entry in raw.values():
            t = str(entry.get("ticker", "")).upper()
            cik = str(entry.get("cik_str", ""))
            if t and cik:
                _cik_cache[t] = cik
    return _cik_cache.get(ticker)
