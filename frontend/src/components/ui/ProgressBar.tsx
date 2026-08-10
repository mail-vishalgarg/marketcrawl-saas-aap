import styles from './ProgressBar.module.css';

interface ProgressBarProps {
  value: number;
  max: number;
  label?: string;
}

export function ProgressBar({ value, max, label }: ProgressBarProps) {
  const pct = Math.min(100, Math.round((value / max) * 100));
  const severity = pct >= 90 ? 'crit' : pct >= 70 ? 'warn' : '';

  return (
    <div className={`${styles.wrap} ${severity ? styles[severity] : ''}`}>
      <div className={styles.labels}>
        <span>{label ?? `${value.toLocaleString()} / ${max.toLocaleString()}`}</span>
        <span>{pct}%</span>
      </div>
      <div className={styles.track}>
        <div className={styles.fill} style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}
