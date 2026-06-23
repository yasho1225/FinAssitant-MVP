import { useState, useEffect } from "react";
import { fetchResearch, fetchAnalytics, fetchHealth } from "./api";
import type { ResearchResponse, AnalyticsResponse } from "./types";
import { TickerSearch } from "./components/TickerSearch";
import { LoadingState } from "./components/LoadingState";
import { MemoReport } from "./components/MemoReport";
import { AnalyticsReport } from "./components/AnalyticsReport";
import { Hero } from "./components/Hero";
import { IconLogo } from "./components/Icons";

type View = "home" | "memo" | "analytics";

export default function App() {
  const [view, setView] = useState<View>("home");
  const [loading, setLoading] = useState(false);
  const [loadingTicker, setLoadingTicker] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [memoData, setMemoData] = useState<ResearchResponse | null>(null);
  const [analyticsData, setAnalyticsData] = useState<AnalyticsResponse | null>(null);
  const [apiStatus, setApiStatus] = useState<"ok" | "error" | "checking">("checking");

  useEffect(() => {
    fetchHealth()
      .then(() => setApiStatus("ok"))
      .catch(() => setApiStatus("error"));
  }, []);

  const handleSearch = async (ticker: string, mode: "memo" | "analytics") => {
    setLoading(true);
    setLoadingTicker(ticker);
    setError(null);
    setMemoData(null);
    setAnalyticsData(null);
    window.scrollTo({ top: 0, behavior: "smooth" });

    try {
      if (mode === "memo") {
        const data = await fetchResearch(ticker);
        setMemoData(data);
        setView("memo");
      } else {
        const data = await fetchAnalytics(ticker);
        setAnalyticsData(data);
        setView("analytics");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
      setView("home");
    } finally {
      setLoading(false);
      setLoadingTicker("");
    }
  };

  const reset = () => {
    setView("home");
    setMemoData(null);
    setAnalyticsData(null);
    setError(null);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <>
      <div className="page-bg" aria-hidden />

      <div className="min-h-screen flex flex-col relative">
        <header className="no-print border-b border-ink-800/60 bg-ink-950/80 backdrop-blur-xl sticky top-0 z-50">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 py-3.5 flex items-center justify-between">
            <button onClick={reset} className="flex items-center gap-3 group">
              <IconLogo className="w-9 h-9 group-hover:scale-105 transition-transform" />
              <div className="text-left hidden sm:block">
                <h1 className="font-display text-lg text-ink-100 leading-tight">FinAssistant</h1>
                <p className="text-[10px] uppercase tracking-[0.15em] text-ink-500">
                  Equity Research
                </p>
              </div>
            </button>

            <div className="flex items-center gap-3">
              <div
                className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] border ${
                  apiStatus === "ok"
                    ? "border-signal-buy/20 text-signal-buy bg-signal-buy/5"
                    : apiStatus === "error"
                      ? "border-signal-sell/20 text-signal-sell bg-signal-sell/5"
                      : "border-ink-700 text-ink-500"
                }`}
              >
                <span
                  className={`w-1.5 h-1.5 rounded-full ${
                    apiStatus === "ok" ? "bg-signal-buy animate-pulse" : "bg-ink-600"
                  }`}
                />
                {apiStatus === "ok" ? "Live" : apiStatus === "error" ? "Offline" : "…"}
              </div>

              {view !== "home" && (
                <button
                  onClick={reset}
                  className="text-sm font-medium text-ink-300 hover:text-ink-100 px-4 py-2 rounded-xl bg-ink-800/80 border border-ink-700/50 hover:border-ink-600 transition-all"
                >
                  ← New Search
                </button>
              )}
            </div>
          </div>
        </header>

        <main
          className={`flex-1 mx-auto w-full px-4 sm:px-6 py-8 md:py-12 ${
            view === "memo" ? "max-w-6xl" : "max-w-4xl"
          }`}
        >
          {view === "home" && !loading && (
            <div className="animate-fade-in">
              <Hero />
              <TickerSearch
                onSubmit={handleSearch}
                loading={loading}
                disabled={apiStatus === "error"}
              />

              {error && (
                <div className="mt-8 max-w-2xl mx-auto p-4 rounded-xl bg-signal-sell/10 border border-signal-sell/25 text-signal-sell text-sm text-center">
                  {error}
                </div>
              )}

              {apiStatus === "error" && (
                <p className="mt-8 text-center text-sm text-ink-500">
                  Start the API:{" "}
                  <code className="font-mono text-accent-teal bg-ink-900 px-2 py-1 rounded-lg border border-ink-700">
                    uvicorn app.main:app --port 8000
                  </code>
                </p>
              )}
            </div>
          )}

          {loading && <LoadingState ticker={loadingTicker} />}

          {view === "memo" && memoData && !loading && <MemoReport data={memoData} />}
          {view === "analytics" && analyticsData && !loading && (
            <AnalyticsReport data={analyticsData} />
          )}
        </main>

        <footer className="no-print border-t border-ink-800/40 py-8 text-center">
          <p className="text-[11px] text-ink-600 max-w-md mx-auto leading-relaxed">
            FinAssistant MVP · Deterministic analytics + AI narrative · Not investment advice
          </p>
        </footer>
      </div>
    </>
  );
}
