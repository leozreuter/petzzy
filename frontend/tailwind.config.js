/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}", // pega todos os arquivos do src
  ],
  theme: {
    extend: {
      colors: {
        petzzy: { blue: "#022037", blue2: "#0b4470" },
        brand: "#FF7E36",
      },
    },
  },
  plugins: [],
};
