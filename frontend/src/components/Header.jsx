import { Link } from 'react-router'

export default function Header() {
  return (
    <header className="header">
      <div className="header__inner">
        <Link to="/" className="logo">Secret<span>Place</span></Link>
      </div>
    </header>
  )
}
