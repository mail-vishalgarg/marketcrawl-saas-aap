# React UI Best Practices

## Folder Layout

```
frontend/src/
├── components/
│   ├── ui/              # Generic, reusable atoms (Button, Input, Card)
│   └── features/        # Domain-specific composites (ProductCard, ApiKeyRow)
├── pages/               # One file per route — thin, just compose components
├── hooks/               # Custom hooks — one concern per file
├── lib/                 # Pure utilities, API client, formatters
├── types/               # Shared TypeScript interfaces and enums
└── main.tsx
```

## Components — one concern, one screen

Each component renders one thing. If you need to scroll to read it, split it.

```tsx
// components/features/ProductCard.tsx
interface ProductCardProps {
  asin: string;
  title: string;
  price: number;
  rating: number;
}

export function ProductCard({ asin, title, price, rating }: ProductCardProps) {
  return (
    <div className="product-card">
      <h3>{title}</h3>
      <PriceTag price={price} />
      <StarRating value={rating} />
    </div>
  );
}
```

- Always name exports (`export function Foo`, not `export default`).
- Props interface directly above the component, not in a separate file unless shared.
- No logic beyond conditional rendering inside JSX — extract to a variable or hook first.

## TypeScript — strict, no escape hatches

```tsx
// Good
const price = data.price as number;  // only if you verified the API shape

// Bad — never
const result: any = response.data;
const el = ref.current!;             // avoid non-null assertion unless truly impossible
```

- Define API response shapes in `src/types/api.ts`; import them everywhere.
- Use discriminated unions for state that has multiple modes:

```ts
type FetchState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; message: string };
```

## Custom Hooks — extract everything stateful

If a component has more than one `useState` or one `useEffect`, move the logic to a hook:

```ts
// hooks/useProductSearch.ts
export function useProductSearch(query: string) {
  const { data, isLoading, error } = useQuery({
    queryKey: ["products", query],
    queryFn: () => api.searchProducts(query),
    enabled: query.length > 2,
  });
  return { products: data?.results ?? [], isLoading, error };
}
```

Rules for hooks:
- Name starts with `use`.
- Returns a plain object with named fields, not a tuple (except `[value, setValue]` pairs).
- One hook per concern; compose hooks in components, not in other hooks.

## Data Fetching — TanStack Query

Use `@tanstack/react-query` for all server state. No manual `useEffect` + `fetch` patterns.

```tsx
// Always set a queryKey that fully describes the request
const { data } = useQuery({
  queryKey: ["product", asin],
  queryFn: () => api.getProduct(asin),
  staleTime: 60_000,          // don't refetch within 1 min
});

// Mutations invalidate related queries
const mutation = useMutation({
  mutationFn: api.createApiKey,
  onSuccess: () => queryClient.invalidateQueries({ queryKey: ["api-keys"] }),
});
```

## API Client — single module, typed

```ts
// lib/api.ts
const BASE = import.meta.env.VITE_API_URL;

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<T>;
}

export const api = {
  getProduct: (asin: string) => request<Product>(`/products/${asin}`),
  searchProducts: (q: string) => request<SearchResponse>(`/products/search?q=${q}`),
};
```

Never call `fetch` directly in a component or hook — always go through `lib/api.ts`.

## State Management

Default order of preference:

1. **Local `useState`** — component-scoped UI state (open/closed, form field).
2. **Lifted state / props** — share between a parent and a few children.
3. **TanStack Query** — anything that comes from the server.
4. **Zustand** — client-only global state (auth token, sidebar collapsed, theme).
   Add Zustand only when you actually need it; don't reach for it by default.

Never put server data in Zustand — that duplicates the cache.

## Forms

Use `react-hook-form` with Zod validation:

```tsx
const schema = z.object({
  email: z.string().email(),
  name: z.string().min(2),
});

const { register, handleSubmit, formState: { errors } } = useForm<z.infer<typeof schema>>({
  resolver: zodResolver(schema),
});
```

- One `useForm` call per form component.
- Validation schema defined outside the component (stable reference).
- Never manually wire `onChange` + `useState` for a form field when `register` exists.

## Performance

Apply these only when there's a measured problem, not by default:

- `React.memo` — wrap a component only if it re-renders with identical props visibly often.
- `useMemo` — memoize expensive computations (>1ms), not simple transforms.
- `useCallback` — only when passing a callback as a prop to a memoised child.

Premature memoisation adds noise without benefit.

## Accessibility Basics

- Every interactive element is a `<button>` or `<a>`, never a `<div onClick>`.
- Images have meaningful `alt` text; decorative images use `alt=""`.
- Form inputs are always associated with a `<label>` (via `htmlFor` + `id`, or wrapping).
- Use semantic HTML (`<nav>`, `<main>`, `<section>`, `<article>`) before reaching for `<div>`.
