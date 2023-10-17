export default defineNuxtPlugin(() => {
    // now available on `nuxtApp.$injected`

    // You can alternatively use this format, which comes with automatic type support
    return {
        provide: {
            injected: (e: string) => 'my injected function ' + e
        }
    }
})
