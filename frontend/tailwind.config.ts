import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: 'class',
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0ea5e9',
          900: '#0c4a6e',
        },
        risk: {
          minimal: '#10b981', // emerald-500
          limited: '#f59e0b', // amber-500
          high: '#ef4444',    // red-500
          unacceptable: '#7f1d1d', // red-900
        },
        surface: {
          light: '#ffffff',
          dark: '#1e293b',    // slate-800
        },
        background: {
          light: '#f8fafc',   // slate-50
          dark: '#0f172a',    // slate-900
        }
      }
    },
  },
  plugins: [],
};
export default config;
