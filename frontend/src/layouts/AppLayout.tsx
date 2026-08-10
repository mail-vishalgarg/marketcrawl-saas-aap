import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import styles from './AppLayout.module.css';

const NAV = [
  { to: '/overview',  icon: '⬡', label: 'Overview'   },
  { to: '/playground', icon: '⚡', label: 'Playground' },
  { to: '/api-keys',  icon: '🔑', label: 'API Keys'   },
  { to: '/docs',      icon: '📄', label: 'Docs'        },
];

export function AppLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleSignout() {
    logout();
    navigate('/login');
  }

  const initials = user?.email?.slice(0, 2).toUpperCase() ?? 'U';

  return (
    <div className={styles.shell}>
      <aside className={styles.sidebar}>
        <div className={styles.logoWrap}>
          <div className={styles.logoIcon}>M</div>
          <span className={styles.logoName}>marketcrawl</span>
        </div>

        <nav className={styles.nav}>
          {NAV.map(({ to, icon, label }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `${styles.navLink}${isActive ? ' ' + styles.active : ''}`
              }
            >
              <span className={styles.navIcon}>{icon}</span>
              {label}
            </NavLink>
          ))}
          <div className={styles.navDivider} />
        </nav>

        <div className={styles.sideFooter}>
          <div className={styles.avatar}>{initials}</div>
          <div className={styles.userInfo}>
            <div className={styles.userEmail}>{user?.email ?? 'user'}</div>
          </div>
          <button className={styles.signout} onClick={handleSignout} title="Sign out">⎋</button>
        </div>
      </aside>

      <main className={styles.content}>
        <Outlet />
      </main>
    </div>
  );
}
