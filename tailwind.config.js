/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily:{
        cursive : ["Pacifico", 'cursive']
      },
      screens : {
        'xxs' : '1px',
        'xs' : '350px'
      }
    },
  },
  plugins: [],
}