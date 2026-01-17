import React, { Suspense } from 'react'
import { Toaster } from 'react-hot-toast'
import ErrorBoundary from './components/ui/ErrorBoundary'
import LoadingSpinner from './components/ui/LoadingSpinner'
import { ThemeProvider } from './contexts/ThemeContext'
import './App.css'
import './styles/theme.css'

// Lazy load AppRouter for better performance
const AppRouter = React.lazy(() => import('./components/AppRouter'))

function App() {
  return (
    <ThemeProvider>
      <div className="App" dir="rtl">
        <ErrorBoundary>
          <Suspense fallback={<LoadingSpinner />}>
            <AppRouter />
          </Suspense>
          <Toaster
          position="top-left"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#134e4a',
              color: '#fff',
              fontSize: '14px',
              fontFamily: 'Cairo, Tajawal, sans-serif',
              borderRadius: '12px',
              boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.2)',
              padding: '12px 16px',
            },
            success: {
              duration: 3000,
              iconTheme: {
                primary: '#10b981',
                secondary: '#fff',
              },
              style: {
                background: '#065f46',
              }
            },
            error: {
              duration: 5000,
              iconTheme: {
                primary: '#f43f5e',
                secondary: '#fff',
              },
              style: {
                background: '#881337',
              }
            },
            loading: {
              iconTheme: {
                primary: '#14b8a6',
                secondary: '#fff',
              },
            },
          }}
        />
      </ErrorBoundary>
    </div>
    </ThemeProvider>
  )
}

export default App
