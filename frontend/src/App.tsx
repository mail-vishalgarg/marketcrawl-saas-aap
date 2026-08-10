import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './hooks/useAuth';
import { AppLayout } from './layouts/AppLayout';
import { Login } from './pages/Login';
import { Overview } from './pages/Overview';
import { Playground } from './pages/Playground';
import { ApiKeys } from './pages/ApiKeys';
import { Docs } from './pages/Docs';

function RequireAuth({ children }: { children: React.ReactNode }) {
  const { user } = useAuth();
  return user ? <>{children}</> : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        element={
          <RequireAuth>
            <AppLayout />
          </RequireAuth>
        }
      >
        <Route index element={<Navigate to="/overview" replace />} />
        <Route path="/overview"   element={<Overview />} />
        <Route path="/playground" element={<Playground />} />
        <Route path="/api-keys"   element={<ApiKeys />} />
        <Route path="/docs"       element={<Docs />} />
      </Route>
      <Route path="*" element={<Navigate to="/overview" replace />} />
    </Routes>
  );
}
