import { Link, useLocation } from 'react-router'
import { useAuth } from '../auth.jsx'
import Icon from './Icon.jsx'
import './Header.css'

export default function Header() {
  const { user, loading, logout } = useAuth()
  const { pathname } = useLocation()
  const isAuthPage = pathname === '/login' || pathname === '/register'

  let actions = null
  if (user) {
    actions = (
      <>
        <div className="header__user">
          <Icon name="user" />
          <span>{user.username}</span>
        </div>
        <button className="btn btn--sm" onClick={() => logout()}>Выйти</button>
        <button className="btn btn--sm btn--ghost" onClick={() => logout(true)}>Выйти со всех устройств</button>
      </>
    )
  } else if (!loading && !isAuthPage) {
    actions = (
      <>
        <Link to="/login" className="btn btn--sm">Войти</Link>
        {!pathname.startsWith('/s/') && <Link to="/register" className="btn btn--sm btn--primary">Регистрация</Link>}
      </>
    )
  }

  return (
    <header className="header">
      <div className="header__inner">
        <Link to="/" className="logo">Secret<span>Place</span></Link>
        <div className="header__actions">{actions}</div>
      </div>
    </header>
  )
}
