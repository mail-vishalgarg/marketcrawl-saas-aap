import styles from './Badge.module.css';

type BadgeVariant = 'default' | 'success' | 'danger' | 'accent' | 'warning';

interface BadgeProps {
  variant?: BadgeVariant;
  children: React.ReactNode;
}

export function Badge({ variant = 'default', children }: BadgeProps) {
  return <span className={`${styles.badge} ${styles[variant]}`}>{children}</span>;
}
