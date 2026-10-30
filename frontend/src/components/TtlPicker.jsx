import { useState } from 'react'
import './TtlPicker.css'

const PRESETS = [
  { label: '5 мин', seconds: 5 * 60 },
  { label: '1 час', seconds: 60 * 60 },
  { label: '12 часов', seconds: 12 * 60 * 60 },
  { label: '1 сутки', seconds: 24 * 60 * 60 },
]

// value и onChange - срок жизни в секундах
export default function TtlPicker({ value, onChange }) {
  const [custom, setCustom] = useState(false)

  return (
    <div className="field">
      <span className="label">Срок жизни</span>
      <div className="ttl">
        {PRESETS.map((preset) => (
          <button
            key={preset.seconds}
            type="button"
            className="btn"
            aria-pressed={!custom && value === preset.seconds}
            onClick={() => {
              setCustom(false)
              onChange(preset.seconds)
            }}
          >
            {preset.label}
          </button>
        ))}
        {custom ? (
          <input className="input ttl__minutes" type="number" min={1} max={24 * 60} required autoFocus
            aria-label="Срок жизни в минутах"
            value={value / 60 || ''} onChange={(e) => onChange(Number(e.target.value) * 60)} />
        ) : (
          <button type="button" className="btn ttl__custom" onClick={() => setCustom(true)}>Своё…</button>
        )}
      </div>
      <span className="hint">{custom ? 'В минутах: от 1 до 1440' : 'От 1 минуты до 1 суток'}</span>
    </div>
  )
}
