import type { AnalysisRequest, AnalysisResponse, CreatedApiKey } from '../types';
import { supabase } from './supabase';

const BASE = (import.meta.env.VITE_API_URL as string | undefined) ?? 'http://localhost:8000';

class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
    this.name = 'ApiError';
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const { data: { session } } = await supabase.auth.getSession();
  const token = session?.access_token;

  const res = await fetch(`${BASE}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(init?.headers ?? {}),
    },
  });

  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText);
    throw new ApiError(res.status, text);
  }

  if (res.status === 204) return undefined as unknown as T;
  return res.json() as Promise<T>;
}

export const api = {
  health: () => request<{ status: string }>('/health'),

  analyze: (body: AnalysisRequest) =>
    request<AnalysisResponse>('/api/v1/agent/analyze', {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  listApiKeys: () =>
    Promise.resolve([
      { id: '1', name: 'Production', prefix: 'mc_live_abc1', createdAt: '2026-07-01T10:00:00Z', lastUsedAt: '2026-08-09T14:22:00Z' },
      { id: '2', name: 'Development', prefix: 'mc_test_def2', createdAt: '2026-07-15T08:30:00Z', lastUsedAt: null },
    ]),

  createApiKey: (name: string): Promise<CreatedApiKey> =>
    Promise.resolve({
      id: crypto.randomUUID(),
      name,
      prefix: `mc_live_${Math.random().toString(36).slice(2, 8)}`,
      createdAt: new Date().toISOString(),
      lastUsedAt: null,
      rawKey: `mc_live_${crypto.randomUUID().replace(/-/g, '')}`,
    }),

  revokeApiKey: (_id: string) => Promise.resolve(),
};

export { ApiError };
