import { useState } from 'react'
import { Link, Navigate, useNavigate } from 'react-router'
import { request } from '../api.js'
import { useAuth } from '../auth.jsx'

export default function Register() {
  const { user, login } = useAuth()
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [password2, setPassword2] = useState('')
  const [error, setError] = useState('')
  const [sending, setSending] = useState(false)

  if (user) {
    return <Navigate to="/" replace />
  }

  async function handleSubmit(event) {
    event.preventDefault()
    if (password !== password2) {
      setError('Пароли не совпадают')
      return
    }
    setError('')
    setSending(true)
    try {
      await request('/auth/register', { method: 'POST', body: { username, password } })
      await login(username, password)
      navigate('/')
    } catch (e) {
      if (e.status === 409) {
        setError('Это имя пользователя уже занято')
      } else if (e.status === 422) {
        setError('Имя должно быть от 3 до 32 символов, пароль - не короче 8 символов')
      } else {
        setError('Не удалось зарегистрироваться, попробуйте ещё раз')
      }
    } finally {
      setSending(false)
    }
  }

  return (
    <main className="center-page">
      <form className="card auth-card form" onSubmit={handleSubmit}>
        <div className="field">
          <h1>Регистрация</h1>
          <p className="muted">Список секретов, изменение и удаление</p>
        </div>
        <div className="field">
          <label className="label" htmlFor="username">Имя пользователя</label>
          <input className="input" id="username" autoComplete="username" required minLength={3} maxLength={32}
            value={username} onChange={(e) => setUsername(e.target.value)} />
          <span className="hint">От 3 до 32 символов</span>
        </div>
        <div className="field">
          <label className="label" htmlFor="password">Пароль</label>
          <input className="input" id="password" type="password" autoComplete="new-password" required minLength={8} maxLength={128}
            value={password} onChange={(e) => setPassword(e.target.value)} />
          <span className="hint">Минимум 8 символов</span>
        </div>
        <div className="field">
          <label className="label" htmlFor="password2">Повторите пароль</label>
          <input className="input" id="password2" type="password" autoComplete="new-password" required
            value={password2} onChange={(e) => setPassword2(e.target.value)} />
        </div>
        {error && <p className="error">{error}</p>}
        <button className="btn btn--primary" type="submit" disabled={sending}>Создать аккаунт</button>
        <p className="form__footer">
          Уже есть аккаунт? <Link to="/login">Войти</Link>
        </p>
      </form>
    </main>
  )
}
