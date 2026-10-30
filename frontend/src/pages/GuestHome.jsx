import { useState } from 'react'
import { Link } from 'react-router'
import CreatedModal from '../components/CreatedModal.jsx'
import SecretForm from '../components/SecretForm.jsx'

export default function GuestHome() {
  const [created, setCreated] = useState(null)

  return (
    <main className="home">
      <div className="home__intro">
        <h1>Поделитесь секретом</h1>
        <p className="muted">Получите одноразовую ссылку. Секрет удалится после первого просмотра или по истечении срока.</p>
      </div>
      <div className="card">
        <SecretForm onCreated={setCreated} />
      </div>
      <p className="form__footer">
        Чтобы видеть список своих секретов, изменять и удалять их, <Link to="/register">зарегистрируйтесь</Link> или <Link to="/login">войдите</Link>.
      </p>
      {created && (
        <CreatedModal created={created} onClose={() => setCreated(null)} onCreateMore={() => setCreated(null)} />
      )}
    </main>
  )
}
