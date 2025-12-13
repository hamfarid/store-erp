/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: ["class"],
  theme: {
    colors: {
        // Primary - Gaara Green
        primary: {
          DEFAULT: '#80AA45',
          50: '#F5F9EF',
          100: '#E8F1D8',
          200: '#D4E5B1',
          300: '#BFD88A',
          400: '#A0C167',
          500: '#80AA45',
          600: '#689030',
          700: '#4F6D24',
          800: '#374B19',
          900: '#1F2A0E',
        },
        // Secondary - Forest Green
        secondary: {
          DEFAULT: '#3B715A',
          50: '#EDF4F1',
          100: '#D4E6DF',
          200: '#A9CDBF',
          300: '#7EB49F',
          400: '#5C9380',
          500: '#3B715A',
          600: '#22523D',
          700: '#1A3E2E',
          800: '#122A1F',
          900: '#0A1610',
        },
        // Accent - Terracotta
        accent: {
          DEFAULT: '#E65E36',
          50: '#FDF3F0',
          100: '#FAE1D9',
          200: '#F5C3B3',
          300: '#F0A58D',
          400: '#EB8267',
          500: '#E65E36',
          600: '#C7451F',
          700: '#943317',
          800: '#62220F',
          900: '#311108',
        },
        // Semantic Colors
        success: '#80AA45',
        warning: '#E65E36',
        danger: '#C7451F',
        info: '#3B715A',
      },
    fontFamily: {
      sans: ['Cairo', 'Tajawal', 'system-ui', 'sans-serif'],
      arabic: ['Cairo', 'Tajawal'],
    },
    // Spacing
    spacing: {
        '0': '0',
        '1': '0.25rem',
        '2': '0.5rem',
        '3': '0.75rem',
        '4': '1rem',
        '5': '1.25rem',
        '6': '1.5rem',
        '8': '2rem',
        '10': '2.5rem',
        '12': '3rem',
        '16': '4rem',
        '20': '5rem',
        '24': '6rem',
      },
    // Border Radius
    borderRadius: {
      'none': '0',
      'sm': '0.125rem',
      DEFAULT: '0.25rem',
      'md': '0.375rem',
      'lg': '0.5rem',
      'xl': '0.75rem',
      '2xl': '1rem',
      'full': '9999px',
    },
    // Shadows
    boxShadow: {
      'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
      DEFAULT: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
      'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
      'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
      '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
      'none': 'none',
    },
    // Transitions from Design Tokens
    transitionDuration: {
      fast: '150ms',
      base: '200ms',
      slow: '300ms',
      slower: '500ms',
    },
    transitionTimingFunction: {
      'ease-in-out': 'cubic-bezier(0.4, 0, 0.2, 1)',
    },
    // Animations
    animation: {
      'fade-in': 'fadeIn 0.5s ease-in-out',
      'slide-up': 'slideUp 0.3s ease-out',
      'slide-down': 'slideDown 0.3s ease-out',
      'slide-left': 'slideLeft 0.3s ease-out',
      'slide-right': 'slideRight 0.3s ease-out',
      'bounce-in': 'bounceIn 0.6s ease-out',
      'scale-in': 'scaleIn 0.2s ease-out',
      'spin-slow': 'spin 3s linear infinite',
    },
    keyframes: {
      fadeIn: {
        '0%': { opacity: '0' },
        '100%': { opacity: '1' },
      },
      slideUp: {
        '0%': { transform: 'translateY(20px)', opacity: '0' },
        '100%': { transform: 'translateY(0)', opacity: '1' },
      },
      slideDown: {
        '0%': { transform: 'translateY(-20px)', opacity: '0' },
        '100%': { transform: 'translateY(0)', opacity: '1' },
      },
      slideLeft: {
        '0%': { transform: 'translateX(20px)', opacity: '0' },
        '100%': { transform: 'translateX(0)', opacity: '1' },
      },
      slideRight: {
        '0%': { transform: 'translateX(-20px)', opacity: '0' },
        '100%': { transform: 'translateX(0)', opacity: '1' },
      },
      bounceIn: {
        '0%': { transform: 'scale(0.3)', opacity: '0' },
        '50%': { transform: 'scale(1.05)' },
        '70%': { transform: 'scale(0.9)' },
        '100%': { transform: 'scale(1)', opacity: '1' },
      },
      scaleIn: {
        '0%': { transform: 'scale(0.95)', opacity: '0' },
        '100%': { transform: 'scale(1)', opacity: '1' },
      },
    },
  },
  plugins: [],
}
