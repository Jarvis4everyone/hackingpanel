import { useEffect } from 'react'
import { CheckCircle, XCircle, AlertCircle, X } from 'lucide-react'

const Toast = ({ message, type = 'success', onClose, duration = 3000 }) => {
  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(() => {
        onClose()
      }, duration)
      return () => clearTimeout(timer)
    }
  }, [duration, onClose])

  const icons = {
    success: CheckCircle,
    error: XCircle,
    warning: AlertCircle,
    info: AlertCircle
  }

  const colors = {
    success: 'bg-hack-green/20 border-hack-green/50 text-hack-green',
    error: 'bg-red-500/20 border-red-500/50 text-red-400',
    warning: 'bg-yellow-400/20 border-yellow-400/50 text-yellow-400',
    info: 'bg-white/20 border-white/50 text-white'
  }

  const Icon = icons[type] || icons.success

  return (
    <div className={`
      fixed top-4 right-4 z-50
      flex items-center gap-3
      px-4 py-3 rounded-lg
      border backdrop-blur-sm
      shadow-2xl animate-slide-in
      ${colors[type] || colors.success}
      max-w-md
    `}>
      <Icon size={20} className="flex-shrink-0" />
      <p className="flex-1 font-mono text-sm">{message}</p>
      <button
        onClick={onClose}
        className="flex-shrink-0 hover:opacity-70 transition-opacity"
      >
        <X size={16} />
      </button>
    </div>
  )
}

export default Toast

