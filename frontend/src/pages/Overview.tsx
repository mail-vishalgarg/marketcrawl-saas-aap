import { useAuth } from '../hooks/useAuth';
import { ProgressBar } from '../components/ui/ProgressBar';
import styles from './Overview.module.css';

const MOCK_STATS = { requests: 142, keys: 2, analyses: 38 };
const MOCK_USAGE = { used: 142, limit: 500, resetDate: 'Sep 1' };
const MOCK_ACTIVITY = [
  { id: 1, text: 'Analysis: "Top 5 phones under $500 in USA"', time: '2 min ago', ok: true },
  { id: 2, text: 'API key created: prod-key-1', time: '1 hr ago', ok: true },
  { id: 3, text: 'Analysis: "Best budget laptops 2024"', time: '3 hr ago', ok: true },
  { id: 4, text: 'Rate limit hit on /agent/analyze', time: '5 hr ago', ok: false },
  { id: 5, text: 'Analysis: "Sony WH-1000XM5 competitors"', time: 'Yesterday', ok: true },
];

export function Overview() {
  const { user } = useAuth();
  const name = user?.email?.split('@')[0] ?? 'there';

  return (
    <div className={styles.page}>
      <h1 className={styles.greeting}>Hey, {name} 👋</h1>
      <p className={styles.sub}>Here's what's happening with your account today.</p>

      <div className={styles.stats}>
        <div className={styles.statCard}>
          <div className={styles.statLabel}>Total Requests</div>
          <div className={styles.statValue}>{MOCK_STATS.requests}</div>
          <div className={styles.statMeta}>This billing period</div>
        </div>
        <div className={styles.statCard}>
          <div className={styles.statLabel}>Active API Keys</div>
          <div className={styles.statValue}>{MOCK_STATS.keys}</div>
          <div className={styles.statMeta}>Across all projects</div>
        </div>
        <div className={styles.statCard}>
          <div className={styles.statLabel}>Analyses Run</div>
          <div className={styles.statValue}>{MOCK_STATS.analyses}</div>
          <div className={styles.statMeta}>Amazon competitive</div>
        </div>
      </div>

      <div className={styles.section}>
        <div className={styles.sectionTitle}>Monthly Usage</div>
        <div className={styles.usageCard}>
          <ProgressBar
            value={MOCK_USAGE.used}
            max={MOCK_USAGE.limit}
            label={`${MOCK_USAGE.used} / ${MOCK_USAGE.limit} requests — resets ${MOCK_USAGE.resetDate}`}
          />
        </div>
      </div>

      <div className={styles.section}>
        <div className={styles.sectionTitle}>Recent Activity</div>
        <div className={styles.activity}>
          {MOCK_ACTIVITY.map(item => (
            <div key={item.id} className={styles.actRow}>
              <span className={`${styles.actDot}${item.ok ? '' : ' ' + styles.error}`} />
              <span className={styles.actText}>{item.text}</span>
              <span className={styles.actTime}>{item.time}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
