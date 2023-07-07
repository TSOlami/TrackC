/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: "jit",
  content: [
    "./webapp/templates/**/*.{html,js}",
    "./node_modules/tw-elements/dist/js/**/*.js"
  ],
  theme: {
    extend: {},
  },
  plugins: [require("tw-elements/dist/plugin.cjs")],
  darkMode: "class"
};

