import { createContext, useContext, useState, useEffect } from 'react'
import { checkAuthStatus, login as apiLogin, logout as apiLogout } from '../services/api'

const AuthContext = createContext(null)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [username, setUsername] = useState(null)

  useEffect(() => {
    // Check if user is already authenticated
    const checkAuth = async () => {
      const token = localStorage.getItem('auth_token')
      if (token) {
        try {
          const status = await checkAuthStatus()
          setIsAuthenticated(status.authenticated)
          setUsername(status.username || null)
        } catch (error) {
          setIsAuthenticated(false)
          setUsername(null)
        }
      } else {
        setIsAuthenticated(false)
        setUsername(null)
      }
      setIsLoading(false)
    }

    checkAuth()
  }, [])

  const login = async (username, password) => {
    console.log('[AuthContext] Login called:', username)
    try {
      const response = await apiLogin(username, password)
      console.log('[AuthContext] Login response:', response)
      localStorage.setItem('auth_token', response.token)
      setIsAuthenticated(true)
      setUsername(username)
      return { success: true }
    } catch (error) {
      console.error('[AuthContext] Login error:', error)
      console.error('[AuthContext] Error response:', error.response)
      return {
        success: false,
        error: error.response?.data?.detail || error.message || 'Login failed'
      }
    }
  }
  }

  const logout = async () => {
    await apiLogout()
    setIsAuthenticated(false)
    setUsername(null)
  }

  return (
    <AuthContext.Provider value={{
      isAuthenticated,
      isLoading,
      username,
      login,
      logout
    }}>
      {children}
    </AuthContext.Provider>
  )
}

