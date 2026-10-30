import { useEffect } from 'react'
import Icon from './Icon.jsx'

// Закрывается по крестику, Esc и клику по затемнённому фону
export default function Modal({ title, icon, subtitle, onClose, children }) {
  useEffect(() => {
    function handleKeyDown(event) {
      if (event.key === 'Escape') {
        onClose()
      }
    }
    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [onClose])

  return (
    // mousedown, а не click: иначе выделение текста мышью с отпусканием на фоне закрывало бы модалку
    <div className="modal-backdrop" onMouseDown={(e) => e.target === e.currentTarget && onClose()}>
      <div className="card modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
        <div className="modal__header">
          <div className="modal__title">
            {icon}
            <div className="field">
              <h2 id="modal-title">{title}</h2>
              {subtitle}
            </div>
          </div>
          <button className="close-btn" aria-label="Закрыть" title="Закрыть" onClick={onClose}>
            <Icon name="x" size={20} />
          </button>
        </div>
        {children}
      </div>
    </div>
  )
}
