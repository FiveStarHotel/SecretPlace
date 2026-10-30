import { Route, Routes } from 'react-router'
import Header from './components/Header.jsx'

export default function App() {
  return (
    <>
      <Header />
      <Routes>
        <Route path="/" element={<main className="center-page"><p className="muted">Скоро здесь будет SecretPlace</p></main>} />
      </Routes>
    </>
  )
}
