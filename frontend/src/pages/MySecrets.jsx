import { useEffect, useState } from 'react'
import { request } from '../api.js'
import CopyButton from '../components/CopyButton.jsx'
import CreatedModal from '../components/CreatedModal.jsx'
import EditModal from '../components/EditModal.jsx'
import Icon from '../components/Icon.jsx'
import Modal from '../components/Modal.jsx'
import SecretForm from '../components/SecretForm.jsx'
import { formatDateTime, formatMinutes, minutesLeft, shortToken } from '../format.js'
import './MySecrets.css'

// с какого остатка времени «Осталось» подсвечивается бейджем
const SOON_MINUTES = 5

export default function MySecrets() {
  const [secrets, setSecrets] = useState(null)
  const [error, setError] = useState('')
  const [now, setNow] = useState(Date.now())
  const [creating, setCreating] = useState(false)
  const [created, setCreated] = useState(null)
  const [editingToken, setEditingToken] = useState(null)

  async function loadSecrets() {
    try {
      const data = await request('/secrets')
      setSecrets(data.secrets)
      setError('')
    } catch {
      setError('Не удалось загрузить секреты')
    }
  }

  useEffect(() => {
    loadSecrets()
  }, [])

  // раз в минуту пересчитываем «Осталось» и убираем истёкшие строки
  useEffect(() => {
    const timer = setInterval(() => setNow(Date.now()), 60 * 1000)
    return () => clearInterval(timer)
  }, [])

  function handleCreated(secret) {
    setCreating(false)
    setCreated(secret)
    loadSecrets()
  }

  async function handleDelete(token) {
    if (!window.confirm('Удалить секрет? Ссылка перестанет работать.')) {
      return
    }
    let failed = false
    try {
      await request(`/secrets/${encodeURIComponent(token)}`, { method: 'DELETE' })
    } catch {
      failed = true
    }
    // список обновляем в любом случае: секрет мог уже быть прочитан
    await loadSecrets()
    if (failed) {
      setError('Не удалось удалить секрет')
    }
  }

  const activeSecrets = secrets?.filter((secret) => new Date(secret.expires_at) > now)

  return (
    <main className="page">
      <div className="page__top">
        <div className="field">
          <h1>Мои секреты</h1>
          <p className="muted">Секрет удаляется после первого прочтения или по истечении срока жизни.</p>
        </div>
        <button className="btn btn--primary" onClick={() => setCreating(true)}>
          <Icon name="plus" />
          Новый секрет
        </button>
      </div>

      {error && <p className="error">{error}</p>}

      {activeSecrets?.length === 0 && (
        <div className="card message-card empty-card">
          <p>У вас пока нет секретов</p>
          <button className="btn btn--primary" onClick={() => setCreating(true)}>Создать первый секрет</button>
        </div>
      )}

      {activeSecrets?.length > 0 && (
        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr>
                <th>Токен</th>
                <th>Создан</th>
                <th>Истекает</th>
                <th>Осталось</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              {activeSecrets.map((secret) => {
                const left = minutesLeft(secret.expires_at, now)
                return (
                  <tr key={secret.token}>
                    <td className="mono">{shortToken(secret.token)}</td>
                    <td className="muted">{formatDateTime(secret.created_at)}</td>
                    <td className="muted">{formatDateTime(secret.expires_at)}</td>
                    <td>{left < SOON_MINUTES ? <span className="badge">{formatMinutes(left)}</span> : formatMinutes(left)}</td>
                    <td>
                      <div className="actions">
                        <CopyButton text={`${window.location.origin}/s/${secret.token}`} label="Копировать ссылку" iconOnly />
                        <button className="btn icon-btn" aria-label="Изменить" title="Изменить" onClick={() => setEditingToken(secret.token)}>
                          <Icon name="pencil" />
                        </button>
                        <button className="btn btn--danger icon-btn" aria-label="Удалить" title="Удалить" onClick={() => handleDelete(secret.token)}>
                          <Icon name="trash" />
                        </button>
                      </div>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}

      {creating && (
        <Modal title="Новый секрет" onClose={() => setCreating(false)}>
          <SecretForm onCreated={handleCreated} onCancel={() => setCreating(false)} />
        </Modal>
      )}
      {created && (
        <CreatedModal
          created={created}
          onClose={() => setCreated(null)}
          onCreateMore={() => {
            setCreated(null)
            setCreating(true)
          }}
        />
      )}
      {editingToken && (
        <EditModal
          token={editingToken}
          onClose={() => setEditingToken(null)}
          onSaved={() => setEditingToken(null)}
        />
      )}
    </main>
  )
}
