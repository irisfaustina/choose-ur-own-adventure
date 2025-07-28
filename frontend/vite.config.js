import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ command, mode }) => {

    const env = loadEnv(mode, process.cwd(), "")

    console.log(env.VITE_DEBUG)

    return {
    plugins: [react()],
    server: { //server options 
      ...(env.VITE_DEBUG === "true" && {
      proxy: {
        "/api": { // everytime we make a request to /api, it will be proxied to http://localhost:8000
          target: "http://localhost:8000",
          changeOrigin: true,
          secure: false
        }
      }
    })
  }
}
})