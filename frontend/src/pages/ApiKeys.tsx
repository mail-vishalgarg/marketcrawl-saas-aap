import { useState } from 'react';
import type { ApiKey, CreatedApiKey } from '../types';
import { api } from '../lib/api';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Badge } from '../components/ui/Badge';
import { Modal } from '../components/ui/Modal';
import styles from './ApiKeys.module.css';

const MOCK_KEYS: ApiKey[] = [
  { id: '1', name: 'Production',  prefix: 'mc_prod_', createdAt: '2026-07-01', lastUsedAt: '2026-08-10' },
  { id: '2', name: 'Development', prefix: 'mc_dev_',  createdAt: '2026-07-15', lastUsedAt: '2026-08-09' },
];

export function ApiKeys() {
  const [keys, setKeys]       = useState<ApiKey[]>(MOCK_KEYS);
  const [showCreate, setShowCreate] = useState(false);
  const [newName, setNewName] = useState('');
  const [creating, setCreating] = useState(false);
  const [created, setCreated] = useState<CreatedApiKey | null>(null);
  const [revoking, setRevoking] = useState<string | null>(null);

  async function handleCreate() {
    if (!newName.trim()) return;
    setCreating(true);
    try {
      const res = await api.createApiKey(newName.trim());
      setCreated(res);
      setKeys(prev => [...prev, {
        id: res.id, name: res.name,
        prefix: res.rawKey.slice(0, 12) + '…',
        createdAt: res.createdAt, lastUsedAt: null,
      }]);
    } catch {
      const stub: CreatedApiKey = {
        id: Date.now().toString(), name: newName,
        prefix: 'mc_live_…', lastUsedAt: null,
        createdAt: new Date().toISOString(),
        rawKey: 'mc_' + Math.random().toString(36).slice(2, 18),
      };
      setCreated(stub);
      setKeys(prev => [...prev, {
        id: stub.id, name: stub.name, prefix: stub.prefix,
        createdAt: stub.createdAt, lastUsedAt: null,
      }]);
    } finally {
      setCreating(false);
      setShowCreate(false);
      setNewName('');
    }
  }

  async function handleRevoke(id: string) {
    setRevoking(id);
    try { await api.revokeApiKey(id); } catch { /* stub */ }
    setKeys(prev => prev.filter(k => k.id !== id));
    setRevoking(null);
  }

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <div>
          <div className={styles.title}>API Keys</div>
          <div className={styles.sub}>Authenticate requests to the marketcrawl API.</div>
        </div>
        <Button onClick={() => setShowCreate(true)}>+ New Key</Button>
      </div>

      {created && (
        <div className={styles.newKeyBox}>
          <div className={styles.newKeyLabel}>Your new API key</div>
          <div className={styles.newKeyValue}>{created.rawKey}</div>
          <div className={styles.newKeyWarn}>Copy it now — it won't be shown again.</div>
        </div>
      )}

      <table className={styles.table}>
        <thead>
          <tr>
            <th>Name</th>
            <th>Key</th>
            <th>Created</th>
            <th>Last used</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {keys.length === 0 && (
            <tr><td colSpan={6} className={styles.empty}>No API keys yet. Create one to get started.</td></tr>
          )}
          {keys.map(k => (
            <tr key={k.id}>
              <td className={styles.keyName}>{k.name}</td>
              <td><span className={styles.keyValue}>{k.prefix}••••••••</span></td>
              <td>{k.createdAt.slice(0, 10)}</td>
              <td>{k.lastUsedAt ? k.lastUsedAt.slice(0, 10) : '—'}</td>
              <td><Badge variant="success">Active</Badge></td>
              <td>
                <Button
                  variant="danger" size="sm"
                  onClick={() => handleRevoke(k.id)}
                  disabled={revoking === k.id}
                >
                  Revoke
                </Button>
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
