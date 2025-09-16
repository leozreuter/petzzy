/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}", // pega todos os arquivos do src
  ],
  theme: {
    extend: {
      fontFamily: {
        baloo: ['"Baloo 2"', "sans-serif"],
      },
      colors: {
        petzzy: { blue: "#022037", blue2: "#0b4470" },
        brand: "#FF7E36",
      },
      screens: {
        tablet: "770px",
        laptop: "1024px",
        desktop: "1280px",
      },
    },
  },
  plugins: [],
};
