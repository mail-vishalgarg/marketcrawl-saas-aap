<!-- This file loads on demand when Claude reads any file inside frontend/. -->
<!-- Keep it under 100 lines. Deep React conventions live in .claude/rules/react.md. -->

# Frontend

## Commands

```bash
npm install          # install deps
npm run dev          # dev server → http://localhost:5173
npm run build        # production build → dist/
npm run lint         # eslint
npm run preview      # preview the production build locally
```

## Layout

```
src/
├── components/
│   ├── ui/          # generic atoms: Button, Input, Card, Badge
│   └── features/    # domain composites: ProductCard, ApiKeyRow
├── pages/           # one file per route — composition only, no logic
├── hooks/           # custom hooks, one concern per file (useProductSearch, etc.)
├── lib/
│   └── api.ts       # single typed fetch client — all HTTP calls live here
└── types/           # shared TypeScript interfaces and discriminated unions
```

## Non-obvious decisions

- `VITE_API_URL` env var points at the backend; set it in `.env` locally.
- All server state via TanStack Query — never `useState` + `useEffect` for fetched data.
- Named exports only — default exports make refactoring harder and break fast refresh.
- `src/lib/api.ts` is the single HTTP boundary — components never call `fetch` directly.
