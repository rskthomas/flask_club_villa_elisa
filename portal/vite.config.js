import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import { VitePWA } from 'vite-plugin-pwa'
const apiURL = 'http://localhost:5001/api'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(), 
    vueJsx(), 
    VitePWA({
      devOptions: { enabled: true },
      manifest: {
        name: 'Club Deportivo Villa Elisa',
        short_name: 'CDVE',
        theme_color: '#ffffff',
        icons: [
          {
            src: 'logo.png',
            sizes: '606x633',
            type: 'image/png'
          },
          {
            src: 'pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: 'pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          },
        ]
      },
      workbox: {
        runtimeCaching: [{
          urlPattern: new RegExp(`.*\/api.*`),
          handler: "CacheFirst",
          options: {
            cacheName: 'api-cache',
            cacheableResponse: {
              statuses: [0, 200]
            },
            expiration: {
              maxEntries: 10,
              maxAgeSeconds: 60 * 60 * 24 * 7
            },
          }
        }]
      }
    }
  )],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 5173
  }
})
