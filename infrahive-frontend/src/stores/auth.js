import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: true,
  }),
  actions: {
    login() {
      this.isAuthenticated = true;
      // In a real app, you'd handle actual authentication logic here
    },
    logout() {
      this.isAuthenticated = false;
      // In a real app, you'd clear tokens, redirect, etc.
    },
  },
});