import React from 'react'
import AppRouter from './components/AppRouter'
import { Toaster } from 'react-hot-toast'
import './App.css'

function AppComplete() {
  return (
    <div className="App">
      <AppRouter />
      <Toaster 
        position="top-left"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
          success: {
            duration: 3000,
            theme: {
              primary: 'green',
              secondary: 'black',
            },
          },
          error: {
            duration: 5000,
            theme: {
              primary: 'red',
              secondary: 'black',
            },
          },
        }}
      />
    </div>
  )
}

export default AppComplete
