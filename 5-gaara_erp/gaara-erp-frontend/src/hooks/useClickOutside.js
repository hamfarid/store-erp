import { useEffect, useRef } from "react"

/**
 * Custom hook to detect clicks outside an element
 * @param {function} handler - Callback function to execute on outside click
 * @param {boolean} enabled - Whether the hook is enabled
 * @returns {React.RefObject} - Ref to attach to the element
 */
export function useClickOutside(handler, enabled = true) {
  const ref = useRef(null)

  useEffect(() => {
    if (!enabled) return

    const handleClickOutside = (event) => {
      if (ref.current && !ref.current.contains(event.target)) {
        handler(event)
      }
    }

    document.addEventListener("mousedown", handleClickOutside)
    document.addEventListener("touchstart", handleClickOutside)

    return () => {
      document.removeEventListener("mousedown", handleClickOutside)
      document.removeEventListener("touchstart", handleClickOutside)
    }
  }, [handler, enabled])

  return ref
}
