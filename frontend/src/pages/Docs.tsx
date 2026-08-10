import { useState } from 'react';
import styles from './Docs.module.css';

const BASE = import.meta.env.VITE_API_URL ?? 'https://marketcrawl-saas-3bgctxs6tq-wl.a.run.app';

const SNIPPETS = {
  curl: `curl -X POST ${BASE}/api/v1/agent/analyze \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer <YOUR_API_KEY>" \\
  -d '{
    "question": "Top 5 phones under $500 in USA",
    "marketplace": "com"
  }'`,

  python: `import httpx

BASE = "${BASE}"
API_KEY = "<YOUR_API_KEY>"

response = httpx.post(
    f"{BASE}/api/v1/agent/analyze",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "question": "Top 5 phones under $500 in USA",
        "marketplace": "com",
    },
)
data = response.json()
print(data["analysis"])`,

  javascript: `const BASE = "${BASE}";
const API_KEY = "<YOUR_API_KEY>";

const res = await fetch(\`\${BASE}/api/v1/agent/analyze\`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: \`Bearer \${API_KEY}\`,
  },
  body: JSON.stringify({
    question: "Top 5 phones under $500 in USA",
    marketplace: "com",
  }),
});
const { analysis } = await res.json();
console.log(analysis);`,
};

type Lang = keyof typeof SNIPPETS;

export function Docs() {
  const [lang, setLang] = useState<Lang>('curl');
  const [copied, setCopied] = useState(false);

  function copy() {
    navigator.clipboard.writeText(SNIPPETS[lang]);
    setCopied(true);
    setTimeout(() => setCopied(false), 1800);
  }

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>API Reference</h1>
      <p className={styles.sub}>Integrate Amazon competitive analysis into your product.</p>

      <h3 className={styles.h3}>Endpoints</h3>
      <div className={styles.endpoint}>
        <div className={styles.endpointRow}>
          <span className={`${styles.method} ${styles.post}`}>POST</span>
          <span className={styles.path}>/api/v1/agent/analyze</span>
        </div>
        <div className={styles.endpointDesc}>
          Run an Amazon competitive analysis. Returns structured markdown analysis from gpt-4o.
          Rate limit: 10 requests/minute per IP.
        </div>
      </div>
      <div className={styles.endpoint}>
        <div className={styles.endpointRow}>
          <span className={styles.method}>GET</span>
          <span className={styles.path}>/api/v1/agent/health</span>
        </div>
        <div className={styles.endpointDesc}>Agent health check — returns model and tools status.</div>
      </div>
      <div className={styles.endpoint}>
        <div className={styles.endpointRow}>
          <span className={styles.method}>GET</span>
          <span className={styles.path}>/health</span>
        </div>
        <div className={styles.endpointDesc}>App health check — used by Cloud Run uptime probe.</div>
      </div>

      <h3 className={styles.h3}>Quick start</h3>
      <div className={styles.tabs}>
        {(Object.keys(SNIPPETS) as Lang[]).map(l => (
          <button
            key={l}
            className={`${styles.tab}${lang === l ? ' ' + styles.active : ''}`}
            onClick={() => setLang(l)}
          >
            {l === 'javascript' ? 'JavaScript' : l === 'python' ? 'Python' : 'cURL'}
          </button>
        ))}
      </div>

      <div className={styles.codeBlock}>
        <div className={styles.codeHeader}>
          <span className={styles.codeLang}>{lang}</span>
          <button className={styles.copyBtn} onClick={copy}>
            {copied ? 'Copied!' : 'Copy'}
          </button>
        </div>
        <pre className={styles.code}>{SNIPPETS[lang]}</pre>
      </div>
    </div>
  );
}
