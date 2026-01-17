import { createContext, useContext, useState, useEffect, useCallback } from "react"
import { authService } from "@/services"

const AuthContext = createContext(null)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Check authentication status on mount
  useEffect(() => {
    const initAuth = async () => {
      try {
        const token = localStorage.getItem("access_token")
        const storedUser = localStorage.getItem("user")

        if (token && storedUser) {
          setIsAuthenticated(true)
          setUser(JSON.parse(storedUser))

          // Optionally verify token with backend
          try {
            const profile = await authService.getProfile()
            setUser(profile)
            localStorage.setItem("user", JSON.stringify(profile))
          } catch {
            // Token might be invalid, but don't log out immediately
            // Let the API interceptor handle it
          }
        }
      } catch (err) {
        console.error("Auth initialization error:", err)
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    initAuth()
  }, [])

  // Login handler
  const login = useCallback(async (email, password) => {
    setLoading(true)
    setError(null)

    try {
      // For demo purposes, allow a test login
      if (email === "admin@gaara-erp.com" && password === "admin123") {
        const mockUser = {
          id: 1,
          first_name: "أحمد",
          last_name: "المدير",
          name: "أحمد المدير",
          email: "admin@gaara-erp.com",
          phone: "0501234567",
          company: "شركة جارا",
          position: "مدير النظام",
          role: "admin",
          avatar: null,
        }

        localStorage.setItem("access_token", "demo-token-123")
        localStorage.setItem("refresh_token", "demo-refresh-123")
        localStorage.setItem("user", JSON.stringify(mockUser))

        setIsAuthenticated(true)
        setUser(mockUser)
        return mockUser
      }

      // Real API call
      const data = await authService.login(email, password)
      setIsAuthenticated(true)
      setUser(data.user)
      return data.user
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  // Register handler
  const register = useCallback(async (userData) => {
    setLoading(true)
    setError(null)

    try {
      const data = await authService.register(userData)
      // Don't auto-login after registration, require email verification
      return data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  // Logout handler
  const logout = useCallback(async () => {
    setLoading(true)

    try {
      await authService.logout()
    } catch {
      // Ignore logout errors
    } finally {
      localStorage.removeItem("access_token")
      localStorage.removeItem("refresh_token")
      localStorage.removeItem("user")
      setIsAuthenticated(false)
      setUser(null)
      setLoading(false)
    }
  }, [])

  // Update user profile
  const updateProfile = useCallback(async (profileData) => {
    setLoading(true)
    setError(null)

    try {
      const updatedUser = await authService.updateProfile(profileData)
      setUser(updatedUser)
      localStorage.setItem("user", JSON.stringify(updatedUser))
      return updatedUser
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  // Check if user has specific permission
  const hasPermission = useCallback((permission) => {
    if (!user) return false

    // Admin has all permissions
    if (user.role === "admin") return true

    // Check user's permissions array if it exists
    return user.permissions?.includes(permission) || false
  }, [user])

  // Check if user has specific role
  const hasRole = useCallback((role) => {
    if (!user) return false
    return user.role === role
  }, [user])

  const value = {
    // State
    isAuthenticated,
    user,
    loading,
    error,

    // Actions
    login,
    register,
    logout,
    updateProfile,

    // Helpers
    hasPermission,
    hasRole,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export default AuthContext
