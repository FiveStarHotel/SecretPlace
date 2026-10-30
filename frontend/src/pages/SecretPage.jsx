import { useState } from 'react'
import { Link, useParams } from 'react-router'
import { request } from '../api.js'
import CopyButton from '../components/CopyButton.jsx'
import Icon from '../components/Icon.jsx'

export default function SecretPage() {
  const { token } = useParams()
  const [secret, setSecret] = useState(null)
  const [gone, setGone] = useState(false)
  const [loading, setLoading] = useState(false)

  // запрос только по кнопке: GET удаляет секрет, а боты-превью ссылок в мессенджерах открывают страницу сами
  async function reveal() {
    setLoading(true)
    try {
      const data = await request(`/secrets/${encodeURIComponent(token)}`)
      setSecret(data.secret)
    } catch {
      setGone(true)
    } finally {
      setLoading(false)
    }
  }

  if (gone) {
    return (
      <main className="center-page">
        <div className="card message-card">
          <div className="circle-icon"><Icon name="alert" size={28} /></div>
          <h1>Секрет недоступен</h1>
          <p>Он уже был прочитан, удалён владельцем или истёк срок его жизни.</p>
          <Link to="/" className="btn btn--primary">Создать свой секрет</Link>
        </div>
      </main>
    )
  }

  if (secret !== null) {
    return (
      <main className="center-page">
        <div className="card secret-card form">
          <h1>Секрет</h1>
          <label className="visually-hidden" htmlFor="secret-value">Текст секрета</label>
          <textarea className="input mono" id="secret-value" readOnly value={secret} />
          <div className="secret-card__footer">
            <span className="warning">Секрет удалён с сервера. Сохраните его - повторно открыть не получится.</span>
            <CopyButton text={secret} />
          </div>
        </div>
      </main>
    )
  }

  return (
    <main className="center-page">
      <div className="card message-card">
        <div className="circle-icon circle-icon--primary"><Icon name="lock" size={28} /></div>
        <h1>Вам передали секрет</h1>
        <p>Его можно просмотреть только один раз. После открытия он будет удалён с сервера.</p>
        <button className="btn btn--lg btn--primary" onClick={reveal} disabled={loading}>Показать секрет</button>
      </div>
    </main>
  )
}
