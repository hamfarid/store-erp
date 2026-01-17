import { describe, it, expect } from 'vitest'

describe('Environment', () => {
  it('should provide jsdom document', () => {
    expect(typeof document).toBe('object')
    expect(document.createElement('div')).toBeInstanceOf(HTMLElement)
  })
})

