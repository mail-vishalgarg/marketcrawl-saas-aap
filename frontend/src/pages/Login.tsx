import { useState } from 'react';
import type { FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import styles from './Login.module.css';

type Mode = 'signin' | 'signup';

export function Login() {
  const { login, signup } = useAuth();
  const navigate = useNavigate();
  const [mode, setMode] = useState<Mode>('signin');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [info, setInfo] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError('');
    setInfo('');
    setLoading(true);
    try {
      if (mode === 'signin') {
        await login(email, password);
        navigate('/overview');
      } else {
        await signup(email, password);
        setInfo('Account created — check your email to confirm, then sign in.');
        setMode('signin');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <div className={styles.logo}>
          <div className={styles.logoIcon}>M</div>
          <span className={styles.logoName}>marketcrawl</span>
        </div>

        <div className={styles.tabs}>
          <button
            className={`${styles.tab}${mode === 'signin' ? ' ' + styles.activeTab : ''}`}
            onClick={() => { setMode('signin'); setError(''); setInfo(''); }}
            type="button"
          >
            Sign in
          </button>
          <button
            className={`${styles.tab}${mode === 'signup' ? ' ' + styles.activeTab : ''}`}
            onClick={() => { setMode('signup'); setError(''); setInfo(''); }}
            type="button"
          >
            Sign up
          </button>
        </div>

        <h1 className={styles.heading}>
          {mode === 'signin' ? 'Welcome back' : 'Create your account'}
        </h1>
        <p className={styles.sub}>
          {mode === 'signin'
            ? 'Sign in to your dashboard'
            : 'Get started with Amazon competitive analysis'}
        </p>

        <form className={styles.form} onSubmit={handleSubmit}>
          {error && <div className={styles.error}>{error}</div>}
          {info  && <div className={styles.infoBox}>{info}</div>}
          <Input
            id="email"
            label="Email"
            type="email"
            placeholder="you@company.com"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
          />
          <Input
            id="password"
            label="Password"
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
            minLength={6}
          />
          <Button type="submit" full disabled={loading}>
            {loading
              ? (mode === 'signin' ? 'Signing in…' : 'Creating account…')
              : (mode === 'signin' ? 'Sign in' : 'Create account')}
          </Button>
        </form>
      </div>
    </div>
  );
}
