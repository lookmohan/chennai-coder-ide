import type { Config } from "tailwindcss";

// `<alpha-value>` lets utilities like bg-primary/90 and border-danger/40 work with CSS-variable colors.
const c = (name: string) => `hsl(var(--${name}) / <alpha-value>)`;

const config: Config = {
  darkMode: ["class"],
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./features/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        background: c("background"),
        foreground: c("foreground"),
        card: c("card"),
        muted: { DEFAULT: c("muted"), foreground: c("muted-foreground") },
        border: c("border"),
        ring: c("ring"),
        primary: { DEFAULT: c("primary"), foreground: c("primary-foreground") },
        danger: { DEFAULT: c("danger"), foreground: c("danger-foreground") },
        success: { DEFAULT: c("success"), foreground: c("success-foreground") },
      },
      borderRadius: { DEFAULT: "var(--radius)", lg: "calc(var(--radius) + 2px)" },
      fontFamily: {
        sans: ["var(--font-sans)", "system-ui", "sans-serif"],
        mono: ["var(--font-mono)", "ui-monospace", "monospace"],
      },
    },
  },
  plugins: [],
};

export default config;
