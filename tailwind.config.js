/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',     // Все шаблоны Django
    './users/**/*.html',
    './products/**/*.html',
    './**/*.js',                 // Вдруг используешь Tailwind в JS
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
