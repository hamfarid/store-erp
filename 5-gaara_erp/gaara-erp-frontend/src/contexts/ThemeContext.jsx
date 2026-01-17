import { createContext, useContext, useState, useEffect, useCallback } from "react"

const ThemeContext = createContext(null)

export const useTheme = () => {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error("useTheme must be used within a ThemeProvider")
  }
  return context
}

export const ThemeProvider = ({ children }) => {
  const [theme, setThemeState] = useState(() => {
    // Check localStorage first
    const stored = localStorage.getItem("theme")
    if (stored) return stored

    // Default to system preference
    return "system"
  })

  const [resolvedTheme, setResolvedTheme] = useState("light")

  // Apply theme to document
  const applyTheme = useCallback((newTheme) => {
    const root = window.document.documentElement
    let effectiveTheme = newTheme

    if (newTheme === "system") {
      effectiveTheme = window.matchMedia("(prefers-color-scheme: dark)").matches
        ? "dark"
        : "light"
    }

    root.classList.remove("light", "dark")
    root.classList.add(effectiveTheme)
    setResolvedTheme(effectiveTheme)

    // Update meta theme-color for mobile browsers
    const metaThemeColor = document.querySelector('meta[name="theme-color"]')
    if (metaThemeColor) {
      metaThemeColor.setAttribute(
        "content",
        effectiveTheme === "dark" ? "#0f172a" : "#ffffff"
      )
    }
  }, [])

  // Handle system theme changes
  useEffect(() => {
    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)")

    const handleChange = () => {
      if (theme === "system") {
        applyTheme("system")
      }
    }

    mediaQuery.addEventListener("change", handleChange)
    return () => mediaQuery.removeEventListener("change", handleChange)
  }, [theme, applyTheme])

  // Apply theme on mount and when theme changes
  useEffect(() => {
    applyTheme(theme)
    localStorage.setItem("theme", theme)
  }, [theme, applyTheme])

  // Set theme function
  const setTheme = useCallback((newTheme) => {
    setThemeState(newTheme)
  }, [])

  // Toggle between light and dark
  const toggleTheme = useCallback(() => {
    setThemeState((prev) => {
      if (prev === "system") {
        // If system, switch to opposite of current resolved
        return resolvedTheme === "dark" ? "light" : "dark"
      }
      return prev === "light" ? "dark" : "light"
    })
  }, [resolvedTheme])

  const value = {
    theme,
    resolvedTheme,
    setTheme,
    toggleTheme,
    isDark: resolvedTheme === "dark",
    isLight: resolvedTheme === "light",
    isSystem: theme === "system",
  }

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  )
}

export default ThemeContext
