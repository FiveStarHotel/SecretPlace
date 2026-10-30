import { formatDateTime } from '../format.js'
import CopyButton from './CopyButton.jsx'
import Icon from './Icon.jsx'
import Modal from './Modal.jsx'
import './CreatedModal.css'

// created - { token, expiresAt } из SecretForm
export default function CreatedModal({ created, onClose, onCreateMore }) {
  const link = `${window.location.origin}/s/${created.token}`
  const icon = (
    <div className="circle-icon circle-icon--primary circle-icon--sm">
      <Icon name="check" size={16} />
    </div>
  )

  return (
    <Modal title="Секрет создан" icon={icon} onClose={onClose}>
      <p className="muted">
        Отправьте ссылку получателю. Её можно открыть только один раз - до {formatDateTime(created.expiresAt)}.
      </p>
      <div className="field">
        <label className="label" htmlFor="link">Ссылка</label>
        <div className="copy-row">
          <input className="input mono" id="link" readOnly value={link} onFocus={(e) => e.target.select()} />
          <CopyButton text={link} />
        </div>
      </div>
      <div className="warning">Не открывайте ссылку сами - после просмотра секрет удалится.</div>
      <div className="actions">
        <button className="btn" onClick={onCreateMore}>Создать ещё</button>
        <button className="btn btn--primary" onClick={onClose}>Готово</button>
      </div>
    </Modal>
  )
}
