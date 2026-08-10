import { useState } from 'react';
import { api } from '../lib/api';
import type { AnalysisResponse } from '../types';
import { Button } from '../components/ui/Button';
import styles from './Playground.module.css';

const EXAMPLES = [
  'Top 5 phones under $500 in USA',
  'Best budget wireless earbuds comparison',
  'Sony WH-1000XM5 top competitors under $200',
];

const MARKETPLACES = [
  { value: 'com', label: 'Amazon US (.com)' },
  { value: 'co.uk', label: 'Amazon UK (.co.uk)' },
  { value: 'de', label: 'Amazon DE (.de)' },
  { value: 'co.jp', label: 'Amazon JP (.co.jp)' },
];

export function Playground() {
  const [query, setQuery] = useState('');
  const [marketplace, setMarketplace] = useState('com');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState('');

  async function handleSubmit() {
    if (!query.trim()) return;
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const res = await api.analyze({ question: query, marketplace });
      setResult(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className={styles.page}>
      <div className={styles.inputPanel}>
        <div>
          <div className={styles.panelTitle}>Playground</div>
          <div className={styles.panelSub}>Ask any Amazon competitive analysis question.</div>
        </div>

        <textarea
          className={styles.textarea}
          placeholder="e.g. Top 5 phones under $500 in USA"
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => { if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) handleSubmit(); }}
        />

        <div className={styles.marketplaceRow}>
          <label className={styles.marketplaceLabel}>Marketplace</label>
          <select className={styles.select} value={marketplace} onChange={e => setMarketplace(e.target.value)}>
            {MARKETPLACES.map(m => <option key={m.value} value={m.value}>{m.label}</option>)}
          </select>
        </div>

        <Button full onClick={handleSubmit} disabled={loading || !query.trim()}>
          {loading ? 'Analyzing…' : 'Run Analysis'}
        </Button>

        <div className={styles.examples}>
          <div className={styles.examplesLabel}>EXAMPLES</div>
          {EXAMPLES.map(ex => (
            <button key={ex} className={styles.exampleBtn} onClick={() => setQuery(ex)}>
              {ex}
            </button>
          ))}
        </div>
      </div>

      <div className={styles.results}>
        {loading && (
          <div className={styles.spinner}>
            <div className={styles.spinnerDot} />
            Querying Amazon data and running analysis…
          </div>
        )}

        {error && <div className={styles.errorBox}>{error}</div>}

        {result && !loading && (
          <>
            <div className={styles.resultHeader}>
              <div>
                <div className={styles.resultQ}>{result.question}</div>
                <div className={styles.resultMeta}>Marketplace: amazon.{result.marketplace} · {new Date(result.generated_at).toLocaleTimeString()}</div>
              </div>
            </div>
            <div className={styles.resultBody}>{result.analysis}</div>
          </>
        )}

        {!result && !loading && !error && (
          <div className={styles.placeholder}>
            <div className={styles.placeholderIcon}>⚡</div>
            <div className={styles.placeholderText}>Run a query to see results here</div>
          </div>
        )}
      </div>
    </div>
  );
}
