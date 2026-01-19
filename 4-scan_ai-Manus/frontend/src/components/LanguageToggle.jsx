/**
 * Language Toggle Component
 * ==========================
 * 
 * A beautiful bilingual toggle for Arabic/English language switching.
 * Features smooth animations, RTL awareness, and accessibility support.
 * 
 * Features:
 * - Animated toggle between AR/EN
 * - Persists preference to localStorage
 * - Updates document dir attribute for RTL
 * - Works with i18n context
 * 
 * @author Global System v35.0
 * @date 2026-01-17
 */

import React, { useState, useEffect, useCallback } from 'react';
import { Globe, Languages } from 'lucide-react';

/**
 * Language Toggle Component
 * 
 * @param {Object} props - Component props
 * @param {string} props.variant - Style variant: 'pill', 'button', 'dropdown'
 * @param {string} props.size - Size: 'sm', 'md', 'lg'
 * @param {Function} props.onLanguageChange - Callback when language changes
 * @param {string} props.className - Additional CSS classes
 */
const LanguageToggle = ({ 
  variant = 'pill', 
  size = 'md',
  onLanguageChange,
  className = '' 
}) => {
  const [language, setLanguage] = useState('ar');
  const [isAnimating, setIsAnimating] = useState(false);

  // Initialize from localStorage
  useEffect(() => {
    const savedLang = localStorage.getItem('language') || 'ar';
    setLanguage(savedLang);
    updateDocumentDirection(savedLang);
  }, []);

  /**
   * Update document direction for RTL support
   */
  const updateDocumentDirection = useCallback((lang) => {
    const dir = lang === 'ar' ? 'rtl' : 'ltr';
    document.documentElement.setAttribute('dir', dir);
    document.documentElement.setAttribute('lang', lang);
    
    // Add language-specific class for custom styling
    document.body.classList.remove('lang-ar', 'lang-en');
    document.body.classList.add(`lang-${lang}`);
  }, []);

  /**
   * Toggle language between AR and EN
   */
  const toggleLanguage = useCallback(() => {
    if (isAnimating) return;
    
    setIsAnimating(true);
    const newLang = language === 'ar' ? 'en' : 'ar';
    
    setLanguage(newLang);
    localStorage.setItem('language', newLang);
    updateDocumentDirection(newLang);
    
    // Callback for parent components
    if (onLanguageChange) {
      onLanguageChange(newLang);
    }

    // Reset animation state
    setTimeout(() => setIsAnimating(false), 300);
  }, [language, isAnimating, onLanguageChange, updateDocumentDirection]);

  /**
   * Set specific language
   */
  const setLanguageValue = useCallback((lang) => {
    if (lang === language || isAnimating) return;
    
    setIsAnimating(true);
    setLanguage(lang);
    localStorage.setItem('language', lang);
    updateDocumentDirection(lang);
    
    if (onLanguageChange) {
      onLanguageChange(lang);
    }

    setTimeout(() => setIsAnimating(false), 300);
  }, [language, isAnimating, onLanguageChange, updateDocumentDirection]);

  // Size classes
  const sizeClasses = {
    sm: 'text-xs py-1 px-2',
    md: 'text-sm py-2 px-3',
    lg: 'text-base py-3 px-4'
  };

  const iconSize = {
    sm: 14,
    md: 18,
    lg: 22
  };

  // Render Pill variant (default)
  if (variant === 'pill') {
    return (
      <div 
        className={`
          inline-flex items-center rounded-full 
          bg-gradient-to-r from-emerald-50 to-teal-50
          dark:from-emerald-900/30 dark:to-teal-900/30
          border border-emerald-200 dark:border-emerald-700
          shadow-sm hover:shadow-md transition-all duration-300
          ${className}
        `}
        role="group"
        aria-label="Language selection"
      >
        <button
          onClick={() => setLanguageValue('ar')}
          className={`
            relative px-3 py-1.5 rounded-full font-semibold
            transition-all duration-300 ease-out
            ${language === 'ar' 
              ? 'bg-emerald-500 text-white shadow-md scale-105' 
              : 'text-emerald-700 dark:text-emerald-300 hover:bg-emerald-100 dark:hover:bg-emerald-800/50'
            }
            ${sizeClasses[size]}
          `}
          aria-pressed={language === 'ar'}
          aria-label="Switch to Arabic"
        >
          <span className="relative z-10 font-arabic">عربي</span>
          {language === 'ar' && (
            <span 
              className={`
                absolute inset-0 rounded-full bg-emerald-400 
                animate-ping opacity-20
              `}
            />
          )}
        </button>
        
        <span className="w-px h-4 bg-emerald-200 dark:bg-emerald-700" />
        
        <button
          onClick={() => setLanguageValue('en')}
          className={`
            relative px-3 py-1.5 rounded-full font-semibold
            transition-all duration-300 ease-out
            ${language === 'en' 
              ? 'bg-emerald-500 text-white shadow-md scale-105' 
              : 'text-emerald-700 dark:text-emerald-300 hover:bg-emerald-100 dark:hover:bg-emerald-800/50'
            }
            ${sizeClasses[size]}
          `}
          aria-pressed={language === 'en'}
          aria-label="Switch to English"
        >
          <span className="relative z-10">EN</span>
          {language === 'en' && (
            <span 
              className={`
                absolute inset-0 rounded-full bg-emerald-400 
                animate-ping opacity-20
              `}
            />
          )}
        </button>
      </div>
    );
  }

  // Render Button variant
  if (variant === 'button') {
    return (
      <button
        onClick={toggleLanguage}
        className={`
          inline-flex items-center gap-2 rounded-lg
          bg-emerald-500 hover:bg-emerald-600 
          text-white font-semibold
          shadow-md hover:shadow-lg
          transform hover:scale-105
          transition-all duration-200 ease-out
          ${sizeClasses[size]}
          ${className}
        `}
        aria-label={`Current language: ${language === 'ar' ? 'Arabic' : 'English'}. Click to switch.`}
      >
        <Globe 
          size={iconSize[size]} 
          className={`transition-transform duration-300 ${isAnimating ? 'rotate-180' : ''}`}
        />
        <span className={`
          inline-block min-w-[2rem] text-center
          transition-all duration-200
          ${isAnimating ? 'opacity-0 scale-90' : 'opacity-100 scale-100'}
        `}>
          {language === 'ar' ? 'عربي' : 'EN'}
        </span>
      </button>
    );
  }

  // Render Dropdown variant
  if (variant === 'dropdown') {
    const [isOpen, setIsOpen] = useState(false);

    return (
      <div className={`relative ${className}`}>
        <button
          onClick={() => setIsOpen(!isOpen)}
          className={`
            inline-flex items-center gap-2 rounded-lg
            bg-white dark:bg-gray-800 
            border border-emerald-200 dark:border-emerald-700
            text-emerald-700 dark:text-emerald-300
            hover:border-emerald-400 dark:hover:border-emerald-500
            shadow-sm hover:shadow-md
            transition-all duration-200
            ${sizeClasses[size]}
          `}
          aria-expanded={isOpen}
          aria-haspopup="listbox"
        >
          <Languages size={iconSize[size]} />
          <span>{language === 'ar' ? 'العربية' : 'English'}</span>
          <svg 
            className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`}
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>

        {isOpen && (
          <>
            {/* Backdrop to close dropdown */}
            <div 
              className="fixed inset-0 z-10" 
              onClick={() => setIsOpen(false)}
            />
            
            {/* Dropdown menu */}
            <div 
              className={`
                absolute ${language === 'ar' ? 'right-0' : 'left-0'} mt-2 
                min-w-[140px] py-1 z-20
                bg-white dark:bg-gray-800 
                border border-emerald-200 dark:border-emerald-700
                rounded-lg shadow-lg
                animate-fadeIn
              `}
              role="listbox"
            >
              <button
                onClick={() => { setLanguageValue('ar'); setIsOpen(false); }}
                className={`
                  w-full px-4 py-2 text-right flex items-center gap-2
                  transition-colors duration-150
                  ${language === 'ar' 
                    ? 'bg-emerald-50 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400' 
                    : 'hover:bg-gray-50 dark:hover:bg-gray-700'
                  }
                `}
                role="option"
                aria-selected={language === 'ar'}
              >
                <span className="w-5 text-center">
                  {language === 'ar' && '✓'}
                </span>
                <span className="font-arabic">العربية</span>
              </button>
              
              <button
                onClick={() => { setLanguageValue('en'); setIsOpen(false); }}
                className={`
                  w-full px-4 py-2 text-left flex items-center gap-2
                  transition-colors duration-150
                  ${language === 'en' 
                    ? 'bg-emerald-50 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400' 
                    : 'hover:bg-gray-50 dark:hover:bg-gray-700'
                  }
                `}
                role="option"
                aria-selected={language === 'en'}
              >
                <span className="w-5 text-center">
                  {language === 'en' && '✓'}
                </span>
                <span>English</span>
              </button>
            </div>
          </>
        )}
      </div>
    );
  }

  return null;
};

/**
 * Hook for accessing current language
 */
export const useLanguage = () => {
  const [language, setLanguage] = useState(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('language') || 'ar';
    }
    return 'ar';
  });

  useEffect(() => {
    const handleStorage = (e) => {
      if (e.key === 'language') {
        setLanguage(e.newValue || 'ar');
      }
    };

    window.addEventListener('storage', handleStorage);
    return () => window.removeEventListener('storage', handleStorage);
  }, []);

  return {
    language,
    isRTL: language === 'ar',
    isArabic: language === 'ar',
    isEnglish: language === 'en'
  };
};

/**
 * Simple translation helper
 */
export const t = (translations, language = null) => {
  const lang = language || localStorage.getItem('language') || 'ar';
  return translations[lang] || translations.ar || Object.values(translations)[0];
};

export default LanguageToggle;
