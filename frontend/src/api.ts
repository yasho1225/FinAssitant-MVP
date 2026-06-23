import type { AnalyticsResponse, ResearchResponse } from "./types";

const API_BASE = "/api/v1";

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(
      typeof err.detail === "string" ? err.detail : `Request failed (${res.status})`
    );
  }
  return res.json();
}

export async function fetchResearch(
  ticker: string,
  newsWindowDays = 60
): Promise<ResearchResponse> {
  const res = await fetch(`${API_BASE}/research`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      ticker: ticker.toUpperCase(),
      news_window_days: newsWindowDays,
      include_peers: true,
    }),
  });
  return handleResponse<ResearchResponse>(res);
}

export async function fetchAnalytics(ticker: string): Promise<AnalyticsResponse> {
  const res = await fetch(`${API_BASE}/analytics/${ticker.toUpperCase()}`);
  return handleResponse<AnalyticsResponse>(res);
}

export async function fetchHealth(): Promise<{ status: string; version: string }> {
  const res = await fetch(`${API_BASE}/health`);
  return handleResponse(res);
}
