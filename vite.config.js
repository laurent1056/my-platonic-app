import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ command }) => ({
  plugins: [react()],
  base: command === 'build' ? '/my-platonic-app/' : '/',
  build: {
    target: 'esnext' // This fixes the "import.meta" warning
  }
}))