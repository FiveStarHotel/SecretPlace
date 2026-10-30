import { Route, Routes } from 'react-router'
import { useAuth } from './auth.jsx'
import Header from './components/Header.jsx'
import GuestHome from './pages/GuestHome.jsx'
import Login from './pages/Login.jsx'
import Register from './pages/Register.jsx'

// на «/» гость видит форму создания, а вошедший пользователь - свои секреты
function Home() {
  const { user, loading } = useAuth()
  if (loading) {
    return null
  }
  return user ? <main className="center-page"><p className="muted">Скоро здесь будут ваши секреты</p></main> : <GuestHome />
}

export default function App() {
  return (
    <>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </>
  )
}
