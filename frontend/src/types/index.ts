/* ── Auth ──────────────────────────────────────────────────────── */
export interface User {
  id: string;
  email: string;
}

/* ── API keys ──────────────────────────────────────────────────── */
export interface ApiKey {
  id: string;
  name: string;
  key_prefix: string;
  created_at: string;
  last_used_at: string | null;
  revoked: boolean;
}

export interface CreatedApiKey extends ApiKey {
  raw_key: string;
}

/* ── Agent ─────────────────────────────────────────────────────── */
export interface AnalysisRequest {
  question: string;
  marketplace?: string;
}

export interface AnalysisResponse {
  analysis: string;
  question: string;
  marketplace: string;
  generated_at: string;
}

/* ── Overview ──────────────────────────────────────────────────── */
export interface UsageStats {
  callsToday: number;
  dailyQuota: number;
}

export interface ActivityItem {
  id: string;
  query: string;
  marketplace: string;
  timestamp: string;
  durationMs: number;
}

/* ── Chat ──────────────────────────────────────────────────────── */
export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

/* ── Products ──────────────────────────────────────────────────── */
export interface ProductResult {
  asin: string;
  title: string;
  price: number;
  currency: string;
  rating: number;
  reviewCount: number;
  isPrime: boolean;
  imageUrl?: string;
}
