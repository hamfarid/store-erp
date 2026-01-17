import { clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs) {
  return twMerge(clsx(inputs))
}

// Format currency with locale support
export function formatCurrency(amount, currency = "SAR", locale = "ar-SA") {
  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency: currency,
  }).format(amount)
}

// Format date with locale support
export function formatDate(date, locale = "ar-SA", options = {}) {
  const defaultOptions = {
    year: "numeric",
    month: "long",
    day: "numeric",
  }
  return new Intl.DateTimeFormat(locale, { ...defaultOptions, ...options }).format(
    new Date(date)
  )
}

// Format relative time
export function formatRelativeTime(date, locale = "ar-SA") {
  const now = new Date()
  const then = new Date(date)
  const diff = now - then
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)

  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: "auto" })

  if (days > 0) return rtf.format(-days, "day")
  if (hours > 0) return rtf.format(-hours, "hour")
  if (minutes > 0) return rtf.format(-minutes, "minute")
  return rtf.format(-seconds, "second")
}

// Format number with locale
export function formatNumber(num, locale = "ar-SA") {
  return new Intl.NumberFormat(locale).format(num)
}

// Format percentage
export function formatPercent(value, locale = "ar-SA") {
  return new Intl.NumberFormat(locale, {
    style: "percent",
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
  }).format(value / 100)
}

// Truncate text with ellipsis
export function truncate(str, length = 50) {
  if (!str) return ""
  return str.length > length ? str.slice(0, length) + "..." : str
}

// Generate random ID
export function generateId(length = 8) {
  return Math.random().toString(36).substring(2, length + 2)
}

// Debounce function
export function debounce(func, wait = 300) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

// Sleep/delay function
export function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

// Check if string is valid email
export function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

// Check if string is valid phone (Saudi format)
export function isValidPhone(phone) {
  return /^(05|5)(5|0|3|6|4|9|1|8|7)([0-9]{7})$/.test(phone)
}

// Get initials from name
export function getInitials(name) {
  if (!name) return ""
  return name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2)
}

// Storage helpers
export const storage = {
  get: (key) => {
    try {
      const item = localStorage.getItem(key)
      return item ? JSON.parse(item) : null
    } catch {
      return null
    }
  },
  set: (key, value) => {
    try {
      localStorage.setItem(key, JSON.stringify(value))
    } catch {
      console.error("Failed to save to localStorage")
    }
  },
  remove: (key) => {
    try {
      localStorage.removeItem(key)
    } catch {
      console.error("Failed to remove from localStorage")
    }
  },
  clear: () => {
    try {
      localStorage.clear()
    } catch {
      console.error("Failed to clear localStorage")
    }
  },
}
