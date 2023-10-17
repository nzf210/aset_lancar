export default defineNuxtRouteMiddleware((to: object, from: object) => {
    console.log('middleware', to.fullPath)
    console.log('middleware', from.fullPath)
})
