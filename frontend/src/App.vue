<script setup>
import { ref, onMounted } from 'vue'
import AuthView from '@/views/AuthView.vue'
import HomeView from '@/views/HomeView.vue'

const isAuthenticated = ref(false)

onMounted(() => {
  const token = localStorage.getItem('access_token')
  if (token) {
    isAuthenticated.value = true
  }
})

const handleLoginSuccess = () => {
  isAuthenticated.value = true
}

const handleLogout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  isAuthenticated.value = false
}
</script>

<template>
  <AuthView
    v-if="!isAuthenticated"
    @login-success="handleLoginSuccess"
  />

  <HomeView
    v-else
    @logout="handleLogout"
  />
</template>
