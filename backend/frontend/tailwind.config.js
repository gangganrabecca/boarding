/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        background: "#0a0a0a",
        card: "#1a1a1a",
        border: "#2a2a2a",
        primary: "#10b981",
        "primary-hover": "#059669",
        text: "#e5e5e5",
        "text-muted": "#a3a3a3",
      },
    },
  },
  plugins: [],
}
