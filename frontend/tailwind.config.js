/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          950: "#04060c",
          900: "#0a0e17",
          850: "#0f141f",
          800: "#151c2c",
          700: "#1c2638",
          600: "#283448",
          500: "#4a5a72",
          400: "#8494a8",
          300: "#b4c0d0",
          200: "#dce3ec",
          100: "#f4f6f9",
        },
        accent: {
          gold: "#d4a853",
          teal: "#3ee8d6",
          blue: "#5b9cf5",
          violet: "#8b7cf8",
        },
        signal: {
          buy: "#34d399",
          hold: "#fbbf24",
          sell: "#f87171",
        },
      },
      fontFamily: {
        display: ['"Instrument Serif"', "Georgia", "serif"],
        sans: ['"Inter"', "system-ui", "sans-serif"],
        mono: ['"IBM Plex Mono"', "monospace"],
      },
      backgroundImage: {
        "grid-pattern":
          "linear-gradient(rgba(62, 232, 214, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(62, 232, 214, 0.03) 1px, transparent 1px)",
        "hero-glow":
          "radial-gradient(ellipse 70% 60% at 50% -10%, rgba(62, 232, 214, 0.12), transparent), radial-gradient(ellipse 50% 40% at 90% 80%, rgba(212, 168, 83, 0.08), transparent)",
      },
      backgroundSize: {
        grid: "64px 64px",
      },
      boxShadow: {
        glow: "0 0 60px -12px rgba(62, 232, 214, 0.2)",
        "glow-gold": "0 0 40px -8px rgba(212, 168, 83, 0.15)",
        card: "0 8px 32px -8px rgba(0, 0, 0, 0.5)",
        inner: "inset 0 1px 0 0 rgba(255,255,255,0.04)",
      },
      animation: {
        "fade-in": "fadeIn 0.6s ease-out forwards",
        "slide-up": "slideUp 0.5s ease-out forwards",
        "slide-in-right": "slideInRight 0.4s ease-out forwards",
        "pulse-soft": "pulseSoft 2.5s ease-in-out infinite",
        shimmer: "shimmer 2s linear infinite",
        "step-pulse": "stepPulse 1.5s ease-in-out infinite",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { opacity: "0", transform: "translateY(20px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        slideInRight: {
          "0%": { opacity: "0", transform: "translateX(12px)" },
          "100%": { opacity: "1", transform: "translateX(0)" },
        },
        pulseSoft: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.5" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
        stepPulse: {
          "0%, 100%": { opacity: "0.4", transform: "scale(1)" },
          "50%": { opacity: "1", transform: "scale(1.02)" },
        },
      },
    },
  },
  plugins: [],
};
