import json
import re
from typing import Any

from openai import OpenAI

from app.config import get_settings
from app.models.schemas import InvestmentMemo, MemoStructuredOutput, Recommendation
from app.orchestrator.prompts import MEMO_USER_PROMPT, SYSTEM_PROMPT


class LLMOrchestrator:
    """Layer C — narrative synthesis only. No calculations or data fetching."""

    def __init__(self) -> None:
        settings = get_settings()
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required for memo generation")
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    def generate_memo(
        self,
        ticker: str,
        analytics: dict[str, Any],
        news_data: dict[str, Any],
        sec_data: dict[str, Any],
    ) -> tuple[InvestmentMemo, MemoStructuredOutput]:
        user_prompt = self._build_prompt(ticker, analytics, news_data, sec_data)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
        )
        raw = response.choices[0].message.content or "{}"
        payload = json.loads(raw)
        return self._parse_response(payload, analytics)

    def _build_prompt(
        self,
        ticker: str,
        analytics: dict[str, Any],
        news_data: dict[str, Any],
        sec_data: dict[str, Any],
    ) -> str:
        market = analytics.get("market", {})
        company_context = json.dumps(
            {
                "name": market.get("company_name"),
                "sector": market.get("sector"),
                "industry": market.get("industry"),
                "summary": (market.get("business_summary") or "")[:1500],
            },
            indent=2,
        )

        # Strip raw series for token efficiency — keep computed metrics only
        analytics_for_llm = _sanitize_analytics(analytics)
        analytics_json = json.dumps(analytics_for_llm, indent=2, default=str)

        articles = news_data.get("data", {}).get("articles", [])[:10]
        news_summary = "\n".join(
            f"- {a.get('title', '')} ({a.get('publisher', '')})" for a in articles
        ) or "No recent news available."

        filings = sec_data.get("data", {}).get("filings", [])[:8]
        sec_summary = "\n".join(
            f"- {f.get('form')} filed {f.get('filing_date')}: {f.get('url')}" for f in filings
        ) or "No SEC filings found."

        peer = analytics.get("peer_comparison", {})
        peer_summary = json.dumps(peer, indent=2, default=str)

        buffett = analytics.get("buffett_signals", {})
        buffett_summary = json.dumps(buffett, indent=2, default=str)

        return MEMO_USER_PROMPT.format(
            ticker=ticker,
            company_context=company_context,
            analytics_json=analytics_json,
            news_summary=news_summary,
            sec_summary=sec_summary,
            peer_summary=peer_summary,
            buffett_summary=buffett_summary,
        )

    def _parse_response(
        self,
        payload: dict[str, Any],
        analytics: dict[str, Any],
    ) -> tuple[InvestmentMemo, MemoStructuredOutput]:
        memo_raw = payload.get("memo", {})
        structured_raw = payload.get("structured", {})

        # Enforce precomputed key metrics — LLM cannot override numbers
        flat = analytics.get("key_metrics_flat", {})
        structured_raw["key_metrics"] = {
            "revenue_cagr": flat.get("revenue_cagr", "N/A"),
            "eps_cagr": flat.get("eps_cagr", "N/A"),
            "net_margin": flat.get("net_margin", "N/A"),
            "roic": flat.get("roic", "N/A"),
            "roe": flat.get("roe", "N/A"),
            "debt_equity": flat.get("debt_equity", "N/A"),
        }

        rec = structured_raw.get("recommendation", "HOLD").upper()
        if rec not in ("BUY", "HOLD", "SELL"):
            rec = "HOLD"
        structured_raw["recommendation"] = rec

        confidence = structured_raw.get("confidence", 0.5)
        try:
            confidence = float(confidence)
            confidence = max(0.0, min(1.0, confidence))
        except (TypeError, ValueError):
            confidence = 0.5
        structured_raw["confidence"] = confidence

        memo = InvestmentMemo(**memo_raw)
        structured = MemoStructuredOutput(
            ticker=structured_raw.get("ticker", analytics.get("ticker", "")),
            recommendation=Recommendation(structured_raw["recommendation"]),
            confidence=structured_raw["confidence"],
            key_metrics=structured_raw["key_metrics"],
            thesis=structured_raw.get("thesis", {"bull": [], "bear": []}),
            risks=structured_raw.get("risks", []),
            catalysts=structured_raw.get("catalysts", []),
            mind_change_triggers=structured_raw.get("mind_change_triggers", []),
        )
        return memo, structured


def _sanitize_analytics(analytics: dict[str, Any]) -> dict[str, Any]:
    """Remove large raw series; keep computed metrics for LLM."""
    cleaned = {}
    for key, val in analytics.items():
        if key in ("growth",):
            cleaned[key] = {k: v for k, v in val.items() if not k.endswith("_series")}
        else:
            cleaned[key] = val
    return cleaned


def _format_peer_valuation(peer: dict[str, Any]) -> str:
    """Human-readable peer comparison for memo narrative."""
    relative = peer.get("relative_valuation", {})
    if not relative:
        return "Peer comparison data unavailable."

    labels = {
        "pe": "P/E",
        "ev_ebitda": "EV/EBITDA",
        "ps": "P/S",
        "net_margin": "Net margin",
        "roe": "ROE",
        "roic": "ROIC",
    }
    pct_keys = {"net_margin", "roe", "roic"}
    vs_labels = {
        "above_peers": "above peer median",
        "below_peers": "below peer median",
        "in_line": "in line with peers",
        "insufficient_data": "insufficient peer data",
    }

    def fmt(key: str, val: float | None) -> str:
        if val is None:
            return "N/A"
        if key in pct_keys:
            return f"{val * 100:.1f}%"
        return f"{val:.2f}x"

    lines = []
    tickers = peer.get("peer_tickers", [])
    if tickers:
        lines.append(f"Peers analyzed: {', '.join(tickers)}.")
    for key, row in relative.items():
        label = labels.get(key, key)
        subj = fmt(key, row.get("subject"))
        med = fmt(key, row.get("peer_median"))
        vs = vs_labels.get(row.get("vs_peers", ""), row.get("vs_peers", ""))
        lines.append(f"{label} at {subj} vs peer median {med} ({vs}).")
    return " ".join(lines)


def generate_offline_memo(
    ticker: str,
    analytics: dict[str, Any],
    news_data: dict[str, Any],
    sec_data: dict[str, Any],
) -> tuple[InvestmentMemo, MemoStructuredOutput]:
    """Deterministic memo template when no LLM API key is available."""
    flat = analytics.get("key_metrics_flat", {})
    market = analytics.get("market", {})
    buffett = analytics.get("buffett_signals", {})
    peer = analytics.get("peer_comparison", {})

    signals_met = buffett.get("signals_met", 0)
    signals_total = buffett.get("signals_total", 6)

    rec = "HOLD"
    confidence = 0.55
    if signals_met >= 4:
        rec = "BUY"
        confidence = 0.65
    elif signals_met <= 1:
        rec = "SELL"
        confidence = 0.6

    name = market.get("company_name") or ticker
    pe = analytics.get("market", {}).get("pe", {}).get("display", "N/A")
    roic = flat.get("roic", "N/A")
    net_margin = flat.get("net_margin", "N/A")

    thesis_bull = [
        f"Revenue CAGR of {flat.get('revenue_cagr')} indicates historical growth trajectory.",
        f"Capital efficiency (ROIC {roic}) supports durable returns on invested capital.",
    ]
    thesis_bear = [
        f"Valuation at P/E {pe} may limit margin of safety.",
        "Macro and competitive risks could pressure forward estimates.",
    ]

    memo = InvestmentMemo(
        executive_summary=(
            f"**Recommendation: {rec}** (Confidence: {confidence:.2f})\n\n"
            f"{name} ({ticker}) shows {signals_met}/{signals_total} Buffett-style soft signals met. "
            f"ROIC at {roic} and net margin at {net_margin} anchor the fundamental view. "
            f"Valuation at P/E {pe} versus peer medians informs the stance."
        ),
        business_overview=(market.get("business_summary") or f"{name} — business overview unavailable.")[:2000],
        financial_health=(
            f"Revenue CAGR (5Y): {flat.get('revenue_cagr')}. "
            f"EPS CAGR (5Y): {flat.get('eps_cagr')}. "
            f"Net margin: {net_margin}. "
            f"ROE: {flat.get('roe')}. ROIC: {roic}. "
            f"Debt/Equity: {flat.get('debt_equity')}. "
            f"FCF margin: {analytics.get('cash_flow', {}).get('fcf_margin', {}).get('display', 'N/A')}."
        ),
        valuation=(
            f"P/E: {pe}. EV/EBITDA: {analytics.get('market', {}).get('ev_ebitda', {}).get('display', 'N/A')}. "
            f"P/S: {analytics.get('market', {}).get('ps', {}).get('display', 'N/A')}. "
            f"{_format_peer_valuation(peer)}"
        ),
        catalysts="Review upcoming earnings, product cycles, and sector macro drivers from news and SEC filings.",
        risks=(
            "1. Margin compression if input costs rise\n"
            "2. Growth deceleration versus historical CAGR\n"
            "3. Leverage increase or liquidity stress"
        ),
        bear_case="Elevated valuation multiples could unwind if growth slows or rates remain higher for longer.",
        what_would_change_my_mind=(
            f"Revenue growth falling below 5% YoY, net margin compression below prior-year levels, "
            f"or debt/equity rising materially above {flat.get('debt_equity')}."
        ),
        data_appendix=_build_appendix_table(analytics),
        citations=[
            "yfinance — price and fundamentals",
            "sec_edgar — SEC filings",
            news_data.get("source", "yfinance") + " — news",
        ],
    )

    structured = MemoStructuredOutput(
        ticker=ticker,
        recommendation=Recommendation(rec),
        confidence=confidence,
        key_metrics=flat,
        thesis={"bull": thesis_bull, "bear": thesis_bear},
        risks=[
            "Margin compression if input costs rise",
            "Growth deceleration versus historical CAGR",
            "Leverage increase or liquidity stress",
        ],
        catalysts=["Upcoming earnings", "Product cycle updates", "Sector macro trends"],
        mind_change_triggers=[
            "Sustained margin compression",
            "Revenue growth deceleration",
            "Balance sheet leverage increase",
        ],
    )
    return memo, structured


def _build_appendix_table(analytics: dict[str, Any]) -> str:
    flat = analytics.get("key_metrics_flat", {})
    computed_at = analytics.get("computed_at", "")
    rows = [
        "| Metric | Value | Source |",
        "|--------|-------|--------|",
    ]
    for name, val in flat.items():
        rows.append(f"| {name} | {val} | yfinance |")
    rows.append(f"\n*Computed at: {computed_at}*")
    return "\n".join(rows)
