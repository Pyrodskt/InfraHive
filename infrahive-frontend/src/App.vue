<template>
  <v-app>
    <AppSidebar />
    <v-main class="d-flex align-center justify-center">
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import AppSidebar from '@/components/AppSidebar.vue';
</script>
