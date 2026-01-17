import { useRef, useEffect } from "react"

/**
 * usePrevious Hook
 * Returns the previous value of a variable
 * @param {any} value - The value to track
 * @returns {any} - Previous value
 */
export function usePrevious(value) {
  const ref = useRef()

  useEffect(() => {
    ref.current = value
  }, [value])

  return ref.current
}
