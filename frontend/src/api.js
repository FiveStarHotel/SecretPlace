const API_URL = '/api/v1'

export class ApiError extends Error {
  constructor(status, message) {
    super(message)
    this.status = status
  }
}

export function saveTokens(tokens) {
  localStorage.setItem('access_token', tokens.access_token)
  localStorage.setItem('refresh_token', tokens.refresh_token)
}

export function clearTokens() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
}

export function hasTokens() {
  return localStorage.getItem('access_token') !== null
}

let refreshing = null

// refresh-токен одноразовый, поэтому параллельные запросы должны дождаться одного общего обновления
function refreshTokens() {
  if (!refreshing) {
    refreshing = request('/auth/refresh', { method: 'POST', body: { refresh_token: localStorage.getItem('refresh_token') } }, false)
      .then((tokens) => {
        saveTokens(tokens)
        return true
      })
      .catch(() => false)
      .finally(() => {
        refreshing = null
      })
  }
  return refreshing
}

// options: method, body (отправляется как JSON), form (отправляется как форма, нужно для /auth/login)
export async function request(path, options = {}, retry = true) {
  const { method = 'GET', body, form } = options
  const headers = {}
  const token = localStorage.getItem('access_token')

  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  let payload
  if (form) {
    payload = new URLSearchParams(form)
  } else if (body) {
    headers['Content-Type'] = 'application/json'
    payload = JSON.stringify(body)
  }

  const response = await fetch(API_URL + path, { method, headers, body: payload })

  if (response.status === 401 && token && retry) {
    if (await refreshTokens()) {
      return request(path, options, false)
    }
    clearTokens()
    // при загрузке приложения просто остаёмся гостем, а в остальных случаях отправляем на вход
    if (path !== '/users/me') {
      window.location.assign('/login')
    }
  }

  const text = await response.text()
  const data = text ? JSON.parse(text) : null

  if (!response.ok) {
    throw new ApiError(response.status, typeof data === 'string' ? data : JSON.stringify(data?.detail))
  }

  return data
}
