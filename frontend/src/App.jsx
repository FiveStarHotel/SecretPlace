import { Route, Routes } from 'react-router'
import Header from './components/Header.jsx'
import Login from './pages/Login.jsx'
import Register from './pages/Register.jsx'

export default function App() {
  return (
    <>
      <Header />
      <Routes>
        <Route path="/" element={<main className="center-page"><p className="muted">Скоро здесь будет SecretPlace</p></main>} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </>
  )
}
