import React, { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Check if user is logged in on app start
    const checkAuthStatus = async () => {
      const token = localStorage.getItem('auth_token')

      if (token) {
        try {
          // التحقق من صحة التوكن مع الخادم
          const response = await fetch('http://172.16.16.27:8000/api/user/verify-token', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          })

          if (response.ok) {
            const data = await response.json()
            if (data.status === 'success') {
              setUser(data.user)
            } else {
              // التوكن غير صحيح
              localStorage.removeItem('auth_token')
              localStorage.removeItem('user')
            }
          } else {
            // التوكن منتهي الصلاحية أو غير صحيح
            localStorage.removeItem('auth_token')
            localStorage.removeItem('user')
          }
        } catch (error) {
          localStorage.removeItem('auth_token')
          localStorage.removeItem('user')
        }
      }
      setIsLoading(false)
    }

    checkAuthStatus()
  }, [])

  const login = (userData, token) => {
    setUser(userData)
    if (token) {
      localStorage.setItem('auth_token', token)
      localStorage.setItem('user', JSON.stringify(userData))
    }
  }

  const logout = async () => {
    try {
      // Call logout API
      await fetch('http://172.16.16.27:8000/api/auth/logout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
        }
      })
      } catch (_) {
      } finally {
      // Clear local state regardless of API call result
      setUser(null)
      localStorage.removeItem('user')
      localStorage.removeItem('auth_token')
    }
  }

  const value = {
    user,
    login,
    logout,
    isAuthenticated: !!user,
    isLoading
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}
