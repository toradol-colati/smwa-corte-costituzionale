/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        serif: ['"Newsreader"', '"Source Serif 4"', 'Georgia', 'serif'],
        sans: ['"Inter"', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      },
      colors: {
        paper: '#FCFCFA',
        ink: '#18181B',
        muted: '#52525B',
        rule: '#E4E4E7',
        primary: '#991B1B',
        accent: '#1E40AF',
      },
    },
  },
  plugins: [],
};
