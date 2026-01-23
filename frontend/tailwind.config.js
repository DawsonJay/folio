/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'bg-primary': '#1E2A26',
        'bg-header': '#2D4A42',
        'ui-base': '#F0F2F1',
        'accent': '#D4A574',
        'ui-secondary': '#5B8A7A',
        'primary-black': '#1E2A26',
        'primary-white': '#E8E8D8',
      },
      fontFamily: {
        'sans': ['Plus Jakarta Sans', 'sans-serif'],
        'mono': ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}

