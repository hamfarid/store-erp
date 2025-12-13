/**
 * P2.62: Keyboard Shortcuts System
 * 
 * React hook and provider for managing keyboard shortcuts across the application.
 */

import {
  createContext,
  useContext,
  useEffect,
  useState,
  useCallback,
  ReactNode,
} from 'react';

// =============================================================================
// Types
// =============================================================================

export interface Shortcut {
  /** Unique identifier for the shortcut */
  id: string;
  /** Key combination (e.g., 'ctrl+s', 'alt+n', 'escape') */
  keys: string;
  /** Description of what the shortcut does */
  description: string;
  /** Category for grouping in help dialog */
  category: string;
  /** Handler function */
  handler: () => void;
  /** Whether the shortcut is enabled */
  enabled?: boolean;
  /** Prevent default browser behavior */
  preventDefault?: boolean;
}

interface ShortcutsContextType {
  shortcuts: Map<string, Shortcut>;
  registerShortcut: (shortcut: Shortcut) => void;
  unregisterShortcut: (id: string) => void;
  enableShortcut: (id: string) => void;
  disableShortcut: (id: string) => void;
  getShortcutsByCategory: () => Record<string, Shortcut[]>;
  showHelp: boolean;
  toggleHelp: () => void;
}

// =============================================================================
// Context
// =============================================================================

const ShortcutsContext = createContext<ShortcutsContextType | null>(null);

export function useShortcuts() {
  const context = useContext(ShortcutsContext);
  if (!context) {
    throw new Error('useShortcuts must be used within ShortcutsProvider');
  }
  return context;
}

// =============================================================================
// Key Parser
// =============================================================================

interface ParsedKey {
  key: string;
  ctrl: boolean;
  alt: boolean;
  shift: boolean;
  meta: boolean;
}

function parseKeyCombo(combo: string): ParsedKey {
  const parts = combo.toLowerCase().split('+');
  const key = parts[parts.length - 1];
  
  return {
    key,
    ctrl: parts.includes('ctrl') || parts.includes('control'),
    alt: parts.includes('alt'),
    shift: parts.includes('shift'),
    meta: parts.includes('meta') || parts.includes('cmd') || parts.includes('command'),
  };
}

function matchesEvent(parsed: ParsedKey, event: KeyboardEvent): boolean {
  const eventKey = event.key.toLowerCase();
  const keyMatches = eventKey === parsed.key || 
                     event.code.toLowerCase() === parsed.key ||
                     event.code.toLowerCase() === `key${parsed.key}`;
  
  return (
    keyMatches &&
    event.ctrlKey === parsed.ctrl &&
    event.altKey === parsed.alt &&
    event.shiftKey === parsed.shift &&
    event.metaKey === parsed.meta
  );
}

function formatShortcut(keys: string): string {
  const isMac = typeof navigator !== 'undefined' && /Mac/.test(navigator.platform);
  
  return keys
    .replace(/ctrl/gi, isMac ? '⌘' : 'Ctrl')
    .replace(/alt/gi, isMac ? '⌥' : 'Alt')
    .replace(/shift/gi, '⇧')
    .replace(/meta|cmd|command/gi, '⌘')
    .replace(/\+/g, ' + ')
    .replace(/escape/gi, 'Esc')
    .replace(/arrowup/gi, '↑')
    .replace(/arrowdown/gi, '↓')
    .replace(/arrowleft/gi, '←')
    .replace(/arrowright/gi, '→');
}

// =============================================================================
// Provider
// =============================================================================

interface ShortcutsProviderProps {
  children: ReactNode;
}

export function ShortcutsProvider({ children }: ShortcutsProviderProps) {
  const [shortcuts, setShortcuts] = useState<Map<string, Shortcut>>(new Map());
  const [showHelp, setShowHelp] = useState(false);

  const registerShortcut = useCallback((shortcut: Shortcut) => {
    setShortcuts((prev) => {
      const next = new Map(prev);
      next.set(shortcut.id, { ...shortcut, enabled: shortcut.enabled !== false });
      return next;
    });
  }, []);

  const unregisterShortcut = useCallback((id: string) => {
    setShortcuts((prev) => {
      const next = new Map(prev);
      next.delete(id);
      return next;
    });
  }, []);

  const enableShortcut = useCallback((id: string) => {
    setShortcuts((prev) => {
      const next = new Map(prev);
      const shortcut = next.get(id);
      if (shortcut) {
        next.set(id, { ...shortcut, enabled: true });
      }
      return next;
    });
  }, []);

  const disableShortcut = useCallback((id: string) => {
    setShortcuts((prev) => {
      const next = new Map(prev);
      const shortcut = next.get(id);
      if (shortcut) {
        next.set(id, { ...shortcut, enabled: false });
      }
      return next;
    });
  }, []);

  const getShortcutsByCategory = useCallback(() => {
    const categories: Record<string, Shortcut[]> = {};
    
    shortcuts.forEach((shortcut) => {
      if (!categories[shortcut.category]) {
        categories[shortcut.category] = [];
      }
      categories[shortcut.category].push(shortcut);
    });
    
    return categories;
  }, [shortcuts]);

  const toggleHelp = useCallback(() => {
    setShowHelp((prev) => !prev);
  }, []);

  // Global keyboard event listener
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      // Ignore when typing in input fields
      const target = event.target as HTMLElement;
      if (
        target.tagName === 'INPUT' ||
        target.tagName === 'TEXTAREA' ||
        target.isContentEditable
      ) {
        // Only allow escape and specific shortcuts
        if (event.key !== 'Escape') {
          return;
        }
      }

      // Check each shortcut
      for (const shortcut of shortcuts.values()) {
        if (!shortcut.enabled) continue;

        const parsed = parseKeyCombo(shortcut.keys);
        
        if (matchesEvent(parsed, event)) {
          if (shortcut.preventDefault !== false) {
            event.preventDefault();
          }
          shortcut.handler();
          return;
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [shortcuts]);

  // Register help shortcut
  useEffect(() => {
    registerShortcut({
      id: 'show-help',
      keys: 'shift+?',
      description: 'Show keyboard shortcuts help',
      category: 'General',
      handler: toggleHelp,
    });

    return () => unregisterShortcut('show-help');
  }, [registerShortcut, unregisterShortcut, toggleHelp]);

  const value: ShortcutsContextType = {
    shortcuts,
    registerShortcut,
    unregisterShortcut,
    enableShortcut,
    disableShortcut,
    getShortcutsByCategory,
    showHelp,
    toggleHelp,
  };

  return (
    <ShortcutsContext.Provider value={value}>
      {children}
      {showHelp && <ShortcutsHelpDialog onClose={toggleHelp} />}
    </ShortcutsContext.Provider>
  );
}

// =============================================================================
// Help Dialog
// =============================================================================

interface ShortcutsHelpDialogProps {
  onClose: () => void;
}

function ShortcutsHelpDialog({ onClose }: ShortcutsHelpDialogProps) {
  const { getShortcutsByCategory } = useShortcuts();
  const categories = getShortcutsByCategory();

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black bg-opacity-50"
        onClick={onClose}
      />
      
      {/* Dialog */}
      <div className="relative bg-white rounded-xl shadow-2xl max-w-2xl w-full mx-4 max-h-[80vh] overflow-hidden">
        <div className="p-6 border-b">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-gray-900">⌨️ Keyboard Shortcuts</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition"
            >
              ✕
            </button>
          </div>
        </div>
        
        <div className="p-6 overflow-y-auto max-h-[60vh]">
          {Object.entries(categories).map(([category, categoryShortcuts]) => (
            <div key={category} className="mb-6 last:mb-0">
              <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">
                {category}
              </h3>
              <div className="space-y-2">
                {categoryShortcuts.map((shortcut) => (
                  <div
                    key={shortcut.id}
                    className="flex items-center justify-between py-2"
                  >
                    <span className="text-gray-700">{shortcut.description}</span>
                    <kbd className="px-3 py-1.5 bg-gray-100 border border-gray-300 rounded-md font-mono text-sm text-gray-800 shadow-sm">
                      {formatShortcut(shortcut.keys)}
                    </kbd>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
        
        <div className="p-4 bg-gray-50 border-t text-center text-sm text-gray-500">
          Press <kbd className="px-2 py-1 bg-white border rounded text-xs">Esc</kbd> to close
        </div>
      </div>
    </div>
  );
}

// =============================================================================
// Hook for Registering Shortcuts
// =============================================================================

interface UseShortcutOptions {
  /** Key combination */
  keys: string;
  /** Handler function */
  handler: () => void;
  /** Description */
  description?: string;
  /** Category */
  category?: string;
  /** Whether enabled */
  enabled?: boolean;
  /** Prevent default */
  preventDefault?: boolean;
  /** Dependencies for the handler */
  deps?: any[];
}

export function useShortcut(id: string, options: UseShortcutOptions) {
  const { registerShortcut, unregisterShortcut } = useShortcuts();

  useEffect(() => {
    registerShortcut({
      id,
      keys: options.keys,
      description: options.description || '',
      category: options.category || 'General',
      handler: options.handler,
      enabled: options.enabled !== false,
      preventDefault: options.preventDefault,
    });

    return () => unregisterShortcut(id);
  }, [id, options.keys, options.enabled, ...(options.deps || [])]);
}

// =============================================================================
// Predefined Shortcuts
// =============================================================================

export const DEFAULT_SHORTCUTS: Omit<Shortcut, 'handler'>[] = [
  // Navigation
  { id: 'go-home', keys: 'alt+h', description: 'Go to home/dashboard', category: 'Navigation' },
  { id: 'go-products', keys: 'alt+p', description: 'Go to products', category: 'Navigation' },
  { id: 'go-invoices', keys: 'alt+i', description: 'Go to invoices', category: 'Navigation' },
  { id: 'go-customers', keys: 'alt+c', description: 'Go to customers', category: 'Navigation' },
  { id: 'go-settings', keys: 'alt+s', description: 'Go to settings', category: 'Navigation' },
  
  // Actions
  { id: 'new-item', keys: 'ctrl+n', description: 'Create new item', category: 'Actions' },
  { id: 'save', keys: 'ctrl+s', description: 'Save current item', category: 'Actions' },
  { id: 'search', keys: 'ctrl+k', description: 'Open search', category: 'Actions' },
  { id: 'refresh', keys: 'ctrl+r', description: 'Refresh data', category: 'Actions' },
  
  // UI
  { id: 'toggle-sidebar', keys: 'ctrl+b', description: 'Toggle sidebar', category: 'UI' },
  { id: 'close-modal', keys: 'escape', description: 'Close modal/dialog', category: 'UI' },
  { id: 'toggle-dark-mode', keys: 'ctrl+shift+d', description: 'Toggle dark mode', category: 'UI' },
];

// =============================================================================
// Exports
// =============================================================================

export { formatShortcut };
export default useShortcut;

