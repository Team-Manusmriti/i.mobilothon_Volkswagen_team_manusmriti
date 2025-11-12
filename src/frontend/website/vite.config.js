import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true // For car display network access
  },
  base: '/i.mobilothon_Volkswagen_team_manusmriti-frontend/', // ✅ must match repo name
  build: {
    outDir: 'dist',
    sourcemap: false,
    minify: 'terser'
  }
})
