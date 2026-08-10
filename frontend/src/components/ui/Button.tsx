import styles from './Button.module.css';

type Variant = 'primary' | 'secondary' | 'danger' | 'ghost';
type Size = 'sm' | 'md' | 'lg';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: Size;
  full?: boolean;
}

export function Button({
  variant = 'primary',
  size = 'md',
  full = false,
  className = '',
  children,
  ...rest
}: ButtonProps) {
  const cls = [
    styles.btn,
    styles[variant],
    size !== 'md' ? styles[size] : '',
    full ? styles.full : '',
    className,
  ].filter(Boolean).join(' ');

  return <button className={cls} {...rest}>{children}</button>;
}
