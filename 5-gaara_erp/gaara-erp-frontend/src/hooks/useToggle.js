import { useState, useCallback } from "react"

/**
 * useToggle Hook
 * Toggle between true/false or multiple values
 * @param {any} initialValue - Initial value (default: false)
 * @returns {[any, Function, Function, Function]} - [value, toggle, setTrue, setFalse]
 */
export function useToggle(initialValue = false) {
  const [value, setValue] = useState(initialValue)

  const toggle = useCallback(() => {
    setValue((prev) => !prev)
  }, [])

  const setTrue = useCallback(() => {
    setValue(true)
  }, [])

  const setFalse = useCallback(() => {
    setValue(false)
  }, [])

  return [value, toggle, setTrue, setFalse]
}
