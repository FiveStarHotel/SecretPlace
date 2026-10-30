import { useState } from 'react'
import { Link, Navigate, useNavigate } from 'react-router'
import { useAuth } from '../auth.jsx'

export default function Login() {
  const { user, login } = useAuth()
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [sending, setSending] = useState(false)

  if (user) {
    return <Navigate to="/" replace />
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setSending(true)
    try {
      await login(username, password)
      navigate('/')
    } catch (e) {
      setError(e.status === 401 ? 'Неверное имя пользователя или пароль' : 'Не удалось войти, попробуйте ещё раз')
    } finally {
      setSending(false)
    }
  }

  return (
    <main className="center-page">
      <form className="card auth-card form" onSubmit={handleSubmit}>
        <div className="field">
          <h1>Вход</h1>
          <p className="muted">Чтобы управлять своими секретами</p>
        </div>
        <div className="field">
          <label className="label" htmlFor="username">Имя пользователя</label>
          <input className="input" id="username" autoComplete="username" required
            value={username} onChange={(e) => setUsername(e.target.value)} />
        </div>
        <div className="field">
          <label className="label" htmlFor="password">Пароль</label>
          <input className="input" id="password" type="password" autoComplete="current-password" required
            value={password} onChange={(e) => setPassword(e.target.value)} />
        </div>
        {error && <p className="error">{error}</p>}
        <button className="btn btn--primary" type="submit" disabled={sending}>Войти</button>
        <p className="form__footer">
          Нет аккаунта? <Link to="/register">Зарегистрироваться</Link>
        </p>
      </form>
    </main>
  )
}
