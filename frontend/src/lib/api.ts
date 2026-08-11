import type { AnalysisRequest, AnalysisResponse, ApiKey, CreatedApiKey } from '../types';
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
    request<ApiKey[]>('/api/v1/api-keys'),

  createApiKey: (name: string) =>
    request<CreatedApiKey>('/api/v1/api-keys', {
      method: 'POST',
      body: JSON.stringify({ name }),
    }),

  revokeApiKey: (id: string) =>
    request<void>(`/api/v1/api-keys/${id}`, { method: 'DELETE' }),
};

export { ApiError };
