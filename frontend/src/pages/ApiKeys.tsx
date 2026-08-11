import { useEffect, useState } from 'react';
import type { ApiKey, CreatedApiKey } from '../types';
import { api } from '../lib/api';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Badge } from '../components/ui/Badge';
import { Modal } from '../components/ui/Modal';
import styles from './ApiKeys.module.css';

export function ApiKeys() {
  const [keys, setKeys]             = useState<ApiKey[]>([]);
  const [loading, setLoading]       = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [newName, setNewName]       = useState('');
  const [creating, setCreating]     = useState(false);
  const [created, setCreated]       = useState<CreatedApiKey | null>(null);
  const [revoking, setRevoking]     = useState<string | null>(null);
  const [error, setError]           = useState('');

  useEffect(() => {
    api.listApiKeys()
      .then(setKeys)
      .catch(() => setError('Failed to load API keys'))
      .finally(() => setLoading(false));
  }, []);

  async function handleCreate() {
    if (!newName.trim()) return;
    setCreating(true);
    try {
      const res = await api.createApiKey(newName.trim());
      setCreated(res);
      setKeys(prev => [res, ...prev]);
    } catch {
      setError('Failed to create key');
    } finally {
      setCreating(false);
      setShowCreate(false);
      setNewName('');
    }
  }

  async function handleRevoke(id: string) {
    setRevoking(id);
    try {
      await api.revokeApiKey(id);
      setKeys(prev => prev.filter(k => k.id !== id));
    } catch {
      setError('Failed to revoke key');
    } finally {
      setRevoking(null);
    }
  }

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <div>
          <div className={styles.title}>API Keys</div>
          <div className={styles.sub}>Authenticate requests to the marketcrawl API.</div>
        </div>
        <Button onClick={() => { setCreated(null); setShowCreate(true); }}>+ New Key</Button>
      </div>

      {error && <div className={styles.errorBox}>{error}</div>}

      {created && (
        <div className={styles.newKeyBox}>
          <div className={styles.newKeyLabel}>Your new API key — copy it now</div>
          <div className={styles.newKeyValue}>{created.raw_key}</div>
          <div className={styles.newKeyWarn}>This is shown once and cannot be recovered.</div>
        </div>
      )}

      <table className={styles.table}>
        <thead>
          <tr>
            <th>Name</th>
            <th>Key prefix</th>
            <th>Created</th>
            <th>Last used</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {loading && (
            <tr><td colSpan={6} className={styles.empty}>Loading…</td></tr>
          )}
          {!loading && keys.length === 0 && (
            <tr><td colSpan={6} className={styles.empty}>No API keys yet. Create one to get started.</td></tr>
          )}
          {keys.map(k => (
            <tr key={k.id}>
              <td className={styles.keyName}>{k.name}</td>
              <td><span className={styles.keyValue}>{k.key_prefix}••••••••</span></td>
              <td>{k.created_at.slice(0, 10)}</td>
              <td>{k.last_used_at ? k.last_used_at.slice(0, 10) : '—'}</td>
              <td>
                <Badge variant={k.revoked ? 'default' : 'success'}>
                  {k.revoked ? 'Revoked' : 'Active'}
                </Badge>
              </td>
              <td>
                {!k.revoked && (
                  <Button
                    variant="danger" size="sm"
                    onClick={() => handleRevoke(k.id)}
                    disabled={revoking === k.id}
                  >
                    Revoke
                  </Button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {showCreate && (
        <Modal
          title="Create API Key"
          onClose={() => setShowCreate(false)}
          footer={
            <>
              <Button variant="secondary" onClick={() => setShowCreate(false)}>Cancel</Button>
              <Button onClick={handleCreate} disabled={creating || !newName.trim()}>
                {creating ? 'Creating…' : 'Create Key'}
              </Button>
            </>
          }
        >
          <div className={styles.formStack}>
            <Input
              id="key-name"
              label="Key name"
              placeholder="e.g. Production, CI/CD"
              value={newName}
              onChange={e => setNewName(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter') handleCreate(); }}
              autoFocus
            />
          </div>
        </Modal>
      )}
    </div>
  );
}
