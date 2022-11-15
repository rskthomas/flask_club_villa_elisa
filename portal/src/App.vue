<template>

  <NavbarView />

  <main>
    <RouterView/>
  </main>

</template>


<script setup>
  import { RouterLink, RouterView } from 'vue-router'
  import NavbarView from './components/NavbarView.vue'
</script>



