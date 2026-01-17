import { useState, useEffect, useCallback } from "react"

/**
 * useFetch Hook
 * Custom hook for fetching data from an API
 * @param {string|Function} urlOrFunction - URL string or function that returns URL
 * @param {Object} options - Fetch options (method, body, headers, etc.)
 * @param {boolean} immediate - Whether to fetch immediately
 * @returns {Object} - { data, loading, error, refetch, reset }
 */
export function useFetch(urlOrFunction, options = {}, immediate = true) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(immediate)
  const [error, setError] = useState(null)

  const fetchData = useCallback(async () => {
    setLoading(true)
    setError(null)

    try {
      const url = typeof urlOrFunction === "function" ? urlOrFunction() : urlOrFunction
      const response = await fetch(url, {
        ...options,
        headers: {
          "Content-Type": "application/json",
          ...options.headers,
        },
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const result = await response.json()
      setData(result)
      return result
    } catch (err) {
      setError(err)
      throw err
    } finally {
      setLoading(false)
    }
  }, [urlOrFunction, JSON.stringify(options)]) // eslint-disable-line react-hooks/exhaustive-deps

  const refetch = useCallback(() => {
    return fetchData()
  }, [fetchData])

  const reset = useCallback(() => {
    setData(null)
    setError(null)
    setLoading(false)
  }, [])

  useEffect(() => {
    if (immediate) {
      fetchData()
    }
  }, [immediate]) // eslint-disable-line react-hooks/exhaustive-deps

  return { data, loading, error, refetch, reset }
}
