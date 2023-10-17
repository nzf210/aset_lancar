<template>
    <div>
        <p>Selamat datang di FE set-lan</p>
        <img src="/img/sim.jpg" alt="img">
        <img src="~/assets/img/aq.png" alt="img2">
    </div>
</template>

<script setup lang="ts">
useUtils('index barang cess')
const {$injected} = useNuxtApp()
console.log($injected('index barang xxxxxx '))
</script>