import { useState, useEffect } from 'react'

/**
 * Custom hook to monitor backend connection status
 * Periodically pings the health endpoint to check connectivity
 */
export const useConnectionStatus = (interval = 30000) => {
  const [isConnected, setIsConnected] = useState(true)
  const [lastChecked, setLastChecked] = useState(null)

  useEffect(() => {
    const checkConnection = async () => {
      try {
        const controller = new AbortController()
        const timeoutId = setTimeout(() => controller.abort(), 5000) // 5 second timeout

        const response = await fetch('/api/health', {
          signal: controller.signal,
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        })

        clearTimeout(timeoutId)

        if (response.ok) {
          setIsConnected(true)
          setLastChecked(new Date())
        } else {
          setIsConnected(false)
        }
      } catch (error) {
        // Connection failed
        setIsConnected(false)
        console.error('Connection check failed:', error.message)
      }
    }

    // Check immediately on mount
    checkConnection()

    // Set up periodic checking
    const intervalId = setInterval(checkConnection, interval)

    // Cleanup
    return () => {
      clearInterval(intervalId)
    }
  }, [interval])

  return { isConnected, lastChecked }
}

export default useConnectionStatus
