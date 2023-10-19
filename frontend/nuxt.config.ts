import { resolve } from 'path';

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  $production: {},
  $development: {},

  runtimeConfig: {

  },

  alias: {
    "@": resolve(__dirname, "/"),
  },

  modules: ["@nuxtjs/tailwindcss", "@nuxt/content"]
})