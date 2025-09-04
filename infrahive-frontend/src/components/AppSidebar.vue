<template>
  <v-navigation-drawer app>
    <v-list>
      <v-list-item to="/home">
        <v-list-item-title>Home</v-list-item-title>
      </v-list-item>
      <v-list-group value="Inventory">
        <template v-slot:activator="{ props }">
          <v-list-item
            v-bind="props"
            title="Inventory"
          ></v-list-item>
        </template>
        <v-list-item to="/inventory/dashboard" title="Dashboard"></v-list-item>
        <v-list-item to="/inventory/websites" title="Websites"></v-list-item>
        <v-list-item to="/inventory/agents" title="Agents"></v-list-item>
        <v-list-item to="/inventory/api" title="API"></v-list-item>
        <v-list-item to="/inventory/health" title="Health"></v-list-item>
      </v-list-group>
      <v-list-item to="/apm">
        <v-list-item-title>APM</v-list-item-title>
      </v-list-item>
      <v-list-item to="/itcm">
        <v-list-item-title>ITCM</v-list-item-title>
      </v-list-item>
      <v-list-item to="/itsm">
        <v-list-item-title>ITSM</v-list-item-title>
      </v-list-item>
      <v-list-item to="/tenant">
        <v-list-item-title>Tenant</v-list-item-title>
      </v-list-item>
      <v-list-item to="/integration">
        <v-list-item-title>Integration</v-list-item-title>
      </v-list-item>
      <!-- Add more navigation links here -->
    </v-list>

    <template v-slot:append>
      <v-list-item v-if="authStore.isAuthenticated" @click="authStore.logout()" color="error">
        <v-list-item-title class="text-center">Logout</v-list-item-title>
      </v-list-item>
      <v-list-item v-else to="/login" color="primary">
        <v-list-item-title class="text-center">Login</v-list-item-title>
      </v-list-item>
    </template>
  </v-navigation-drawer>
</template>

<script setup>
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();
</script>

<style scoped>
/* Add any specific styles for the sidebar here */
</style>
