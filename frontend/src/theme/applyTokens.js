// FILE: frontend/src/theme/applyTokens.js | PURPOSE: Apply design tokens as CSS variables at runtime | OWNER: UI Team | RELATED: src/ui/theme/tokens.json, src/main.jsx | LAST-AUDITED: 2025-10-29

import tokens from '../ui/theme/tokens.json'

function toKebab(str) {
  return String(str).replace(/[^a-zA-Z0-9]+/g, '-').replace(/([a-z0-9])([A-Z])/g, '$1-$2').toLowerCase()
}

function isNumber(val) {
  return typeof val === 'number' && isFinite(val)
}

function flatten(obj, path = []) {
  const entries = []
  for (const key of Object.keys(obj)) {
    const val = obj[key]
    const p = [...path, key]
    if (val && typeof val === 'object' && !Array.isArray(val)) {
      entries.push(...flatten(val, p))
    } else {
      entries.push([p, val])
    }
  }
  return entries
}

function valueWithUnit(keyPath, value) {
  // Add px for spacing/size/radius numbers
  const joined = keyPath.join('.')
  if (isNumber(value)) {
    if (/(spacing|size|radius|lineHeight)/.test(joined)) return `${value}px`
    return String(value)
  }
  return String(value)
}

function buildCSSVariables() {
  const lines = []
  // Base tokens
  const base = []
  for (const [keyPath, value] of flatten({
    color: tokens.color,
    typography: tokens.typography,
    spacing: tokens.spacing,
    radius: tokens.radius,
    shadow: tokens.shadow,
    motion: tokens.motion,
    breakpoint: tokens.breakpoint,
    zIndex: tokens.zIndex,
    opacity: tokens.opacity,
  })) {
    const varName = `--${toKebab(keyPath.join('-'))}`
    base.push(`  ${varName}: ${valueWithUnit(keyPath, value)};`)
  }
  lines.push(':root {')
  lines.push(...base)
  lines.push('}')

  // Theme variables (light as default overrides)
  if (tokens.themes && tokens.themes.light) {
    const light = []
    for (const [keyPath, value] of flatten(tokens.themes.light, ['theme'])) {
      const varName = `--${toKebab(keyPath.join('-'))}`
      light.push(`  ${varName}: ${String(value)};`)
    }
    lines.push(':root {')
    lines.push(...light)
    lines.push('}')
  }

  // Dark overrides under .dark
  if (tokens.themes && tokens.themes.dark) {
    const dark = []
    for (const [keyPath, value] of flatten(tokens.themes.dark, ['theme'])) {
      const varName = `--${toKebab(keyPath.join('-'))}`
      dark.push(`  ${varName}: ${String(value)};`)
    }
    lines.push('.dark {')
    lines.push(...dark)
    lines.push('}')
  }

  return lines.join('\n')
}

export default function applyTokens() {
  if (typeof document === 'undefined') return
  const STYLE_ID = 'app-design-tokens'
  let styleEl = document.getElementById(STYLE_ID)
  const css = buildCSSVariables()
  if (!styleEl) {
    styleEl = document.createElement('style')
    styleEl.id = STYLE_ID
    document.head.appendChild(styleEl)
  }
  styleEl.textContent = css
}

