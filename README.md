# FinAssistant MVP

AI Equity Research Agent that generates institutional-quality investment memos using **deterministic financial analytics** + **LLM narrative synthesis**.

## Core Principle

> The LLM writes narrative only. All numbers are computed in the analytics layer.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Layer C — LLM Orchestrator (interpretation + memo only)    │
├─────────────────────────────────────────────────────────────┤
│  Layer B — Analytics Engine (pure computation, no LLM)      │
├─────────────────────────────────────────────────────────────┤
│  Layer A — Data Collectors (yfinance, SEC EDGAR, news)      │
└─────────────────────────────────────────────────────────────┘
```

## Repository Structure

```
app/
├── main.py                 # FastAPI application
├── config.py               # Environment settings
├── api/routes.py           # REST endpoints
├── collectors/             # Layer A — data fetching
│   ├── price.py
│   ├── income_statement.py
│   ├── balance_sheet.py
│   ├── cash_flow.py
│   ├── sec_filings.py
│   ├── news.py
│   └── peers.py
├── analytics/              # Layer B — deterministic metrics
│   ├── engine.py
│   ├── growth.py
│   ├── profitability.py
│   ├── capital_efficiency.py
│   ├── cash_flow_metrics.py
│   ├── balance_sheet_metrics.py
│   └── market_metrics.py
├── orchestrator/           # Layer C — LLM narrative
│   ├── llm.py
│   └── prompts.py
├── services/
│   └── research_service.py # End-to-end pipeline
└── models/
    ├── schemas.py          # Pydantic contracts
    └── database.py         # Postgres persistence (optional)
tests/
docker-compose.yml          # Postgres + Redis
requirements.txt
```

## Quick Start

### 1. Install dependencies

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Build the frontend

```bash
cd frontend
npm install
npm run build
cd ..
```

### 3. Configure environment

```bash
copy .env.example .env
```

Edit `.env`:
- `OPENAI_API_KEY` — required for full LLM memos (offline template used if unset)
- `SEC_USER_AGENT` — your email (SEC EDGAR policy)
- `DATABASE_URL` — optional Postgres connection

### 3. Start infrastructure (optional)

```bash
docker compose up -d
```

### 4. Run the API

```bash
uvicorn app.main:app --reload --port 8000
```

Open **http://localhost:8000** for the web UI, or http://localhost:8000/docs for API docs.

### Frontend development (hot reload)

```bash
# Terminal 1 — API
uvicorn app.main:app --reload --port 8000

# Terminal 2 — Vite dev server (proxies /api to :8000)
cd frontend && npm run dev
```

Open http://localhost:5173 during development.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/research` | Full investment memo |
| `GET` | `/api/v1/analytics/{ticker}` | Analytics only (no LLM) |
| `GET` | `/api/v1/health` | Health check |

### Example: Generate memo

```bash
curl -X POST http://localhost:8000/api/v1/research \
  -H "Content-Type: application/json" \
  -d "{\"ticker\": \"AAPL\", \"news_window_days\": 60}"
```

### Example: Analytics only

```bash
curl http://localhost:8000/api/v1/analytics/MSFT
```

## Output Contract

Every memo includes:

1. Executive Summary (BUY/HOLD/SELL + confidence)
2. Business Overview
3. Financial Health
4. Valuation
5. Catalysts
6. Risks
7. Bear Case
8. What Would Change My Mind
9. Data Appendix (timestamped, source-linked)
10. Citations

Plus structured JSON with `recommendation`, `confidence`, `key_metrics`, `thesis`, `risks`, `catalysts`, `mind_change_triggers`.

## Computed Metrics

| Category | Metrics |
|----------|---------|
| Growth | Revenue CAGR (5Y), EPS CAGR (5Y) |
| Profitability | Gross / Operating / Net margin |
| Capital Efficiency | ROE, ROIC |
| Cash Flow | FCF, FCF margin, FCF conversion |
| Balance Sheet | Debt/Equity, Net Debt/EBITDA, Interest coverage |
| Market | P/E, EV/EBITDA, P/S, 1Y/3Y/5Y returns, volatility, max drawdown |

## Data Sources

| Data | Source |
|------|--------|
| Price & fundamentals | [yfinance](https://github.com/ranaroussi/yfinance) |
| SEC filings | [SEC EDGAR](https://www.sec.gov/edgar) |
| News | yfinance (NewsAPI optional) |
| Peers | yfinance + sector mapping |

## Testing

```bash
pytest tests/ -v
```

## Design Constraints

- No quality scores or weighted indices
- Buffett signals are soft screening (narrative only, never filters)
- LLM cannot override precomputed `key_metrics`
- 100% of numbers traceable to deterministic analytics
- US equities only (MVP scope)

## License

MIT
