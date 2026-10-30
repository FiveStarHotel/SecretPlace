import { useState } from 'react'
import Icon from './Icon.jsx'

// После копирования на 2 секунды показывает «Скопировано». iconOnly - квадратная кнопка для таблицы
export default function CopyButton({ text, label = 'Копировать', iconOnly = false, className = 'btn btn--primary' }) {
  const [copied, setCopied] = useState(false)

  async function handleClick() {
    await navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  if (iconOnly) {
    return (
      <button type="button" className="btn icon-btn icon-btn--copy" aria-label={label} title={copied ? 'Скопировано' : label} onClick={handleClick}>
        <Icon name={copied ? 'check' : 'copy'} />
      </button>
    )
  }

  return (
    <button type="button" className={className} onClick={handleClick}>
      <Icon name={copied ? 'check' : 'copy'} size={16} />
      {copied ? 'Скопировано' : label}
    </button>
  )
}
