import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
    plugins: [react()],
    server: { //server options 
      proxy: {
        "/api": { // everytime we make a request to /api, it will be proxied to http://localhost:8000
          target: "http://localhost:8000",
          changeOrigin: true,
          secure: false
        }
      }
    }
})