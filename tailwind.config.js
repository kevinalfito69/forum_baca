/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["templates/**/*.{html,js}", "postingan/templates/*.{html,js}", "user/templates/*.{html,js}", "*/templates/*.{html,js}"],
  daisyui: {
    themes: ["light", "dark", "cupcake", "coffee",],
  },
  theme: {
    extend: {},
  },
  plugins: [require("daisyui"), require('@tailwindcss/typography'),],
}

