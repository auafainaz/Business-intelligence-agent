/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,jsx}",
    "./components/**/*.{js,jsx}"
  ],
  theme: {
    extend: {
      colors: {
        ink: "#05070b",
        graphite: "#0b0f18",
        platinum: "#e7ecf6",
        mist: "#9aa7bb",
        cyan: "#77e4f2",
        blue: "#7aa7ff",
        gold: "#e7c873"
      },
      boxShadow: {
        glow: "0 0 80px rgba(119, 228, 242, 0.16)",
        panel: "0 28px 80px rgba(0, 0, 0, 0.35)"
      }
    }
  },
  plugins: []
};
