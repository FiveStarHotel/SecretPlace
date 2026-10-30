// 31.10.2026 15:05
export function formatDateTime(date) {
  return new Date(date).toLocaleString('ru-RU', {
    day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit',
  }).replace(',', '')
}
