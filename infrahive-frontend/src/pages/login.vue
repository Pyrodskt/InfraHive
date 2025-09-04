<template>
  <v-container fluid fill-height>
    <v-row align="center" justify="center">
      <v-col align-self-center cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Login</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form>
              <v-text-field
                label="Username"
                name="username"
                prepend-icon="mdi-account"
                type="text"
                v-model="username"
              ></v-text-field>

              <v-text-field
                label="Password"
                name="password"
                prepend-icon="mdi-lock"
                type="password"
                v-model="password"
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="login">Login</v-btn>
            <v-btn color="secondary" @click="loginWithMicrosoft">Login with Microsoft</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const username = ref('');
const password = ref('');
const authStore = useAuthStore();
const router = useRouter();

const login = () => {
  // Handle login logic here
  console.log('Username:', username.value);
  console.log('Password:', password.value);
  // In a real app, you'd send this to an API endpoint and check credentials
  // For demonstration, we'll just set isAuthenticated to true
  authStore.login();
  router.push('/home');
};

const loginWithMicrosoft = () => {
  // Handle Microsoft login logic here
  console.log('Initiating Microsoft login...');
  // This would typically involve redirecting to Microsoft's authentication endpoint
  // or using a library like MSAL.js
  // For demonstration, we'll just set isAuthenticated to true
  authStore.login();
  router.push('/home');
};
</script>

<style scoped>
html, body, #app, .v-application {
  height: 100%;
}
</style>
