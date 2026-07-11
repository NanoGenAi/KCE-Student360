/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Karpagam College of Engineering (KCE) Portal Palette
        kce: {
          orange: '#C76F2B',
          'orange-dark': '#A8561F',
          teal: '#214C55',
          'teal-dark': '#163941',
          'light-grey': '#E5E5E5',
          bg: '#F7F7F7',
          white: '#FFFFFF',
          border: '#D1D5DB',
          text: '#111827',
          muted: '#6B7280',
          success: '#15803D',
          warning: '#D97706',
          danger: '#B91C1C',
        },
        // Portfolio Dark Theme Palette
        portfolio: {
          bg: '#0F0F10',           // Full dark background
          panel: '#171719',        // Dark sidebar panel
          card: '#202024',         // Rounded dark cards
          border: '#2E2E33',       // Dark borders
          text: '#F5F5F5',         // Primary text
          muted: '#A1A1AA',        // Secondary text
          accent: '#F5C542',       // Gold highlight line
          'accent-dark': '#D4A017', // Gold secondary accent
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
