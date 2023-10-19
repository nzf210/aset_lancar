export default defineEventHandler(async (event) => {
    console.log('get aset', event);

    return {
        "data": "success"
    }
})