<script setup>
import { RouterLink, RouterView } from "vue-router";
import NavbarView from "./components/NavbarView.vue";
import Footer from "./components/Footer.vue";
</script>
<template>
  <NavbarView />
  <main id="parent">
    <RouterView/>
  </main>
  <Footer />
</template>

<style>
/*this will center all components inside main. Im not good with css so this is the only way i made it work
Change it later, -Thomas*/
#parent {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
}
</style>

