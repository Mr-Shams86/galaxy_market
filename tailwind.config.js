/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',      // Все шаблоны Django
    './users/**/*.html',          // Шаблоны в users/
    './products/**/*.html',       // Шаблоны в products/
    './orders/**/*.html',         // шаблоны заказов
    './**/*.js',                  // Скрипты с Tailwind-классами
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
