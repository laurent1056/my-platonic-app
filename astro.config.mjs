import { defineConfig } from 'astro/config'
import sitemap from '@astrojs/sitemap'
import vercel from '@astrojs/vercel'
import tailwindcss from '@tailwindcss/vite'

const site = process.env.SITE_URL || 'https://my-platonic-app.vercel.app'

export default defineConfig({
  site,
  trailingSlash: 'always',
  adapter: vercel(),
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
})
