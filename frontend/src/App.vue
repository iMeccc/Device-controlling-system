<script setup>
import { RouterView } from 'vue-router';
// The onMounted logic is no longer needed here, as the router guard now handles it.
</script>

<template>
  <!-- RouterView is the placeholder where our pages like Login, Dashboard etc. will be rendered -->
  <RouterView />
</template>

<style>
  /* We can add some basic global styles here */
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
  }
</style>