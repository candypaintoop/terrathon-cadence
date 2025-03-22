/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
    theme: {
      extend: {
        colors: {
          teal: '#00796b',
          'seafoam-green': '#a7ffeb',
          yellow: '#ffeb3b',
        },
      },
    },
    plugins: [],
  };
  