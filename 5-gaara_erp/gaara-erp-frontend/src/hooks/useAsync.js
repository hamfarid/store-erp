import { useState, useEffect, useCallback } from "react"

/**
 * useAsync Hook
 * Handles async operations with loading, error, and data states
 * @param {Function} asyncFunction - The async function to execute
 * @param {boolean} immediate - Whether to execute immediately
 * @returns {Object} - { execute, data, loading, error, reset }
 */
export function useAsync(asyncFunction, immediate = false) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(immediate)
  const [error, setError] = useState(null)

  const execute = useCallback(
    async (...args) => {
      setLoading(true)
      setError(null)
      try {
        const result = await asyncFunction(...args)
        setData(result)
        return result
      } catch (err) {
        setError(err)
        throw err
      } finally {
        setLoading(false)
      }
    },
    [asyncFunction]
  )

  const reset = useCallback(() => {
    setData(null)
    setError(null)
    setLoading(false)
  }, [])

  useEffect(() => {
    if (immediate) {
      execute()
    }
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  return { execute, data, loading, error, reset }
}
