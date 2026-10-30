import { createContext, useContext, useEffect, useState } from 'react'
import { clearTokens, hasTokens, request, saveTokens } from './api.js'

const AuthContext = createContext(null)

// Хранит текущего пользователя и даёт любому компоненту функции входа и выхода через useAuth()
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  async function loadUser() {
    if (!hasTokens()) {
      setUser(null)
      return
    }
    try {
      const me = await request('/users/me')
      // без валидного токена бэкенд отвечает заглушкой с id = -1
      setUser(me.id === -1 ? null : me)
    } catch {
      setUser(null)
    }
  }

  useEffect(() => {
    loadUser().finally(() => setLoading(false))
  }, [])

  async function login(username, password) {
    const tokens = await request('/auth/login', { method: 'POST', form: { username, password } })
    saveTokens(tokens)
    await loadUser()
  }

  async function logout(everywhere = false) {
    const path = everywhere ? '/auth/logout-all' : '/auth/logout'
    try {
      await request(path, { method: 'POST', body: { refresh_token: localStorage.getItem('refresh_token') } })
    } finally {
      clearTokens()
      setUser(null)
    }
  }

  return (
    <AuthContext value={{ user, loading, login, logout }}>
      {children}
    </AuthContext>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
