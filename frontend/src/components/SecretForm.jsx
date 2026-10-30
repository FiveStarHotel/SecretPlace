import { useState } from 'react'
import { request } from '../api.js'
import TtlPicker from './TtlPicker.jsx'

const SECRET_MAX_LENGTH = 4096

// Форма создания секрета. С onCancel рисуется как модалка (Отмена/Создать), без него - как форма на главной
export default function SecretForm({ onCreated, onCancel }) {
  const [secret, setSecret] = useState('')
  const [ttl, setTtl] = useState(60 * 60)
  const [error, setError] = useState('')
  const [sending, setSending] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setSending(true)
    try {
      const { token } = await request('/secrets', { method: 'POST', body: { secret, time_to_live: ttl } })
      setSecret('')
      onCreated({ token, expiresAt: new Date(Date.now() + ttl * 1000) })
    } catch (e) {
      setError(e.status === 422 ? 'Проверьте текст секрета и срок жизни' : 'Не удалось создать секрет, попробуйте ещё раз')
    } finally {
      setSending(false)
    }
  }

  return (
    <form className="form" onSubmit={handleSubmit}>
      <div className="field">
        <label className="label" htmlFor="secret">Текст секрета</label>
        <textarea className="input" id="secret" placeholder="Пароль, ключ, заметка…" required autoFocus={Boolean(onCancel)}
          maxLength={SECRET_MAX_LENGTH} value={secret} onChange={(e) => setSecret(e.target.value)} />
        <div className="field__footer">
          <span className="hint">{secret.length} / {SECRET_MAX_LENGTH}</span>
        </div>
      </div>
      <TtlPicker value={ttl} onChange={setTtl} />
      {error && <p className="error">{error}</p>}
      {onCancel ? (
        <div className="actions">
          <button type="button" className="btn" onClick={onCancel}>Отмена</button>
          <button type="submit" className="btn btn--primary" disabled={sending}>Создать</button>
        </div>
      ) : (
        <button type="submit" className="btn btn--lg btn--primary" disabled={sending}>Создать ссылку</button>
      )}
    </form>
  )
}
