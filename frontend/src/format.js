// 31.10.2026 15:05
export function formatDateTime(date) {
  return new Date(date).toLocaleString('ru-RU', {
    day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit',
  }).replace(',', '')
}

// a8f3…c21e
export function shortToken(token) {
  return `${token.slice(0, 4)}…${token.slice(-4)}`
}

// сколько минут осталось до даты, с округлением вверх
export function minutesLeft(date, now) {
  return Math.ceil((new Date(date) - now) / 60000)
}

// 42 мин, 3 ч 5 мин
export function formatMinutes(minutes) {
  if (minutes < 60) {
    return `${minutes} мин`
  }
  return `${Math.floor(minutes / 60)} ч ${minutes % 60} мин`
}
