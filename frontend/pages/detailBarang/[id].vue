<template>
    <div>//detailBarang/[id].vue {{ $route.params.id }}</div>
</template>

<script>
const route = useRoute();
console.log(route.params.id)
export default {
    layout: 'detailBarang'
}
</script>