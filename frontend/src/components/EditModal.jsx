import { useState } from 'react'
import { request } from '../api.js'
import { shortToken } from '../format.js'
import Modal from './Modal.jsx'

const SECRET_MAX_LENGTH = 4096

export default function EditModal({ token, onClose, onSaved }) {
  const [secret, setSecret] = useState('')
  const [error, setError] = useState('')
  const [sending, setSending] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setSending(true)
    try {
      await request(`/secrets/${encodeURIComponent(token)}`, { method: 'PUT', body: { secret } })
      onSaved()
    } catch (e) {
      setError(e.status === 404 ? 'Секрет уже прочитан или истёк' : 'Не удалось сохранить, попробуйте ещё раз')
    } finally {
      setSending(false)
    }
  }

  return (
    <Modal title="Изменить секрет" subtitle={<span className="mono muted">{shortToken(token)}</span>} onClose={onClose}>
      <form className="form" onSubmit={handleSubmit}>
        <div className="field">
          <label className="label" htmlFor="new-secret">Новый текст секрета</label>
          <textarea className="input" id="new-secret" placeholder="Введите новый текст" required autoFocus
            maxLength={SECRET_MAX_LENGTH} value={secret} onChange={(e) => setSecret(e.target.value)} />
          <div className="field__footer">
            <span className="hint">Старый текст не показывается. Срок жизни не меняется.</span>
            <span className="hint">{secret.length} / {SECRET_MAX_LENGTH}</span>
          </div>
        </div>
        {error && <p className="error">{error}</p>}
        <div className="actions">
          <button type="button" className="btn" onClick={onClose}>Отмена</button>
          <button type="submit" className="btn btn--primary" disabled={sending}>Сохранить</button>
        </div>
      </form>
    </Modal>
  )
}
