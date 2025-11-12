/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
         cyan: {
          500: '#06b6d4',
          600: '#0891b2',
        },
        emerald: {
          500: '#10b981',
          600: '#059669',
        },
        purple: {
          500: '#a855f7',
          600: '#9333ea',
        },
        blue: {
          500: '#3b82f6',
          600: '#2563eb',
        },
        gray: {
          950: '#030712',
          900: '#111827',
          800: '#1F2937',
          700: '#374151',
          600: '#4B5563',
          500: '#6B7280',
          400: '#9CA3AF',
          300: '#D1D5DB',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      animation: {
        'pulse': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'progress': 'progress 3s ease-in-out infinite',
      },
      keyframes: {
        pulse: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '.5' },
        },
        progress: {
          '0%': { width: '0%' },
          '50%': { width: '60%' },
          '100%': { width: '0%' },
        },
      },
    },
  },
  plugins: [],
}