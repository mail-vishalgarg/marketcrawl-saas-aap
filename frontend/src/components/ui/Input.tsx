import styles from './Input.module.css';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
}

export function Input({ label, id, className = '', ...rest }: InputProps) {
  return (
    <div className={styles.wrap}>
      {label && <label className={styles.label} htmlFor={id}>{label}</label>}
      <input id={id} className={`${styles.input} ${className}`} {...rest} />
    </div>
  );
}
