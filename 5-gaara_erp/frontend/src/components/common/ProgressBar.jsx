import React, { useState, createContext, useContext } from 'react'
import './ProgressBar.css'

// Progress Context for managing multiple progress operations
const ProgressContext = createContext()

export const ProgressProvider = ({ children }) => {
  const [operations, setOperations] = useState([])

  const startOperation = (id, config = {}) => {
    const operation = {
      id,
      progress: 0,
      status: 'running',
      message: 'جاري المعالجة...',
      startTime: Date.now(),
      ...config
    }
    
    setOperations(prev => [...prev.filter(op => op.id !== id), operation])
    return id
  }

  const updateOperation = (id, updates) => {
    setOperations(prev => prev.map(op => 
      op.id === id ? { ...op, ...updates } : op
    ))
  }

  const completeOperation = (id, message = 'تم بنجاح') => {
    updateOperation(id, { 
      progress: 100, 
      status: 'completed', 
      message,
      endTime: Date.now()
    })
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
      setOperations(prev => prev.filter(op => op.id !== id))
    }, 3000)
  }

  const failOperation = (id, message = 'فشل في العملية') => {
    updateOperation(id, { 
      status: 'failed', 
      message,
      endTime: Date.now()
    })
  }

  const removeOperation = (id) => {
    setOperations(prev => prev.filter(op => op.id !== id))
  }

  return (
    <ProgressContext.Provider value={{
      operations,
      startOperation,
      updateOperation,
      completeOperation,
      failOperation,
      removeOperation
    }}>
      {children}
    </ProgressContext.Provider>
  )
}

// Basic Progress Bar Component
export const ProgressBar = ({
  progress = 0,
  variant = 'primary',
  size = 'medium',
  showPercentage = true,
  showMessage = true,
  message = '',
  animated = true,
  striped = false,
  className = ''
}) => {
  const progressValue = Math.min(Math.max(progress, 0), 100)
  
  const progressClass = `
    progress-bar
    progress-bar--${variant}
    progress-bar--${size}
    ${animated ? 'progress-bar--animated' : ''}
    ${striped ? 'progress-bar--striped' : ''}
    ${className}
  `.trim()

  return (
    <div className={progressClass}>
      {showMessage && message && (
        <div className="progress-bar__message">{message}</div>
      )}
      
      <div className="progress-bar__track">
        <div 
          className="progress-bar__fill"
          style={{ width: `${progressValue}%` }}
        >
          {showPercentage && (
            <span className="progress-bar__percentage">
              {Math.round(progressValue)}%
            </span>
          )}
        </div>
      </div>
    </div>
  )
}

// Circular Progress Component
export const CircularProgress = ({
  progress = 0,
  size = 120,
  strokeWidth = 8,
  variant = 'primary',
  showPercentage = true,
  children
}) => {
  const progressValue = Math.min(Math.max(progress, 0), 100)
  const radius = (size - strokeWidth) / 2
  const circumference = radius * 2 * Math.PI
  const strokeDasharray = circumference
  const strokeDashoffset = circumference - (progressValue / 100) * circumference

  const colorMap = {
    primary: '#007bff',
    success: '#28a745',
    warning: '#ffc107',
    danger: '#dc3545',
    info: '#17a2b8'
  }

  return (
    <div className="circular-progress" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="circular-progress__svg">
        {/* Background circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="#e9ecef"
          strokeWidth={strokeWidth}
        />
        
        {/* Progress circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={colorMap[variant]}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={strokeDasharray}
          strokeDashoffset={strokeDashoffset}
          className="circular-progress__circle"
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
        />
      </svg>
      
      <div className="circular-progress__content">
        {children || (showPercentage && (
          <span className="circular-progress__percentage">
            {Math.round(progressValue)}%
          </span>
        ))}
      </div>
    </div>
  )
}

// Step Progress Component
export const StepProgress = ({ steps, currentStep, variant: _variant = 'primary' }) => {
  return (
    <div className="step-progress">
      {steps.map((step, index) => {
        const isCompleted = index < currentStep
        const isCurrent = index === currentStep
        const isUpcoming = index > currentStep

        return (
          <div key={index} className="step-progress__step">
            <div className={`
              step-progress__indicator
              ${isCompleted ? 'step-progress__indicator--completed' : ''}
              ${isCurrent ? 'step-progress__indicator--current' : ''}
              ${isUpcoming ? 'step-progress__indicator--upcoming' : ''}
            `}>
              {isCompleted ? (
                <i className="fas fa-check"></i>
              ) : (
                <span>{index + 1}</span>
              )}
            </div>
            
            <div className="step-progress__content">
              <div className="step-progress__title">{step.title}</div>
              {step.description && (
                <div className="step-progress__description">{step.description}</div>
              )}
            </div>
            
            {index < steps.length - 1 && (
              <div className={`
                step-progress__connector
                ${isCompleted ? 'step-progress__connector--completed' : ''}
              `}></div>
            )}
          </div>
        )
      })}
    </div>
  )
}

// Progress Modal for long operations
export const ProgressModal = ({ 
  isOpen, 
  onClose, 
  title = 'جاري المعالجة',
  progress = 0,
  message = '',
  canCancel = false,
  onCancel
}) => {
  if (!isOpen) return null

  return (
    <div className="progress-modal-backdrop">
      <div className="progress-modal">
        <div className="progress-modal__header">
          <h3 className="progress-modal__title">{title}</h3>
          {canCancel && (
            <button 
              className="progress-modal__close"
              onClick={onCancel || onClose}
            >
              <i className="fas fa-times"></i>
            </button>
          )}
        </div>
        
        <div className="progress-modal__body">
          <CircularProgress 
            progress={progress} 
            size={80}
            variant="primary"
          />
          
          <div className="progress-modal__details">
            <ProgressBar 
              progress={progress}
              message={message}
              animated={true}
              striped={true}
            />
          </div>
        </div>
        
        {canCancel && (
          <div className="progress-modal__footer">
            <button 
              className="progress-modal__cancel"
              onClick={onCancel || onClose}
            >
              إلغاء
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

// Hook for using progress operations
export const useProgress = () => {
  const context = useContext(ProgressContext)
  if (!context) {
    throw new Error('useProgress must be used within a ProgressProvider')
  }
  return context
}

// Hook for managing a single progress operation
export const useProgressOperation = (id) => {
  const { operations, startOperation, updateOperation, completeOperation, failOperation } = useProgress()
  const operation = operations.find(op => op.id === id)

  const start = (config) => startOperation(id, config)
  const update = (updates) => updateOperation(id, updates)
  const complete = (message) => completeOperation(id, message)
  const fail = (message) => failOperation(id, message)

  return {
    operation,
    start,
    update,
    complete,
    fail,
    isRunning: operation?.status === 'running',
    isCompleted: operation?.status === 'completed',
    isFailed: operation?.status === 'failed'
  }
}

// Progress Tracker Component for displaying all active operations
export const ProgressTracker = () => {
  const { operations } = useProgress()
  const activeOperations = operations.filter(op => op.status === 'running')

  if (activeOperations.length === 0) return null

  return (
    <div className="progress-tracker">
      <div className="progress-tracker__header">
        <h4>العمليات الجارية ({activeOperations.length})</h4>
      </div>
      
      <div className="progress-tracker__list">
        {activeOperations.map(operation => (
          <div key={operation.id} className="progress-tracker__item">
            <div className="progress-tracker__info">
              <span className="progress-tracker__message">{operation.message}</span>
              <span className="progress-tracker__percentage">{Math.round(operation.progress)}%</span>
            </div>
            <ProgressBar 
              progress={operation.progress}
              size="small"
              showPercentage={false}
              showMessage={false}
              animated={true}
            />
          </div>
        ))}
      </div>
    </div>
  )
}

export default ProgressBar
