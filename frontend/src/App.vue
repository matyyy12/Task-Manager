<script setup>
import { ref, onMounted } from 'vue'
import { RouterView, useRouter } from 'vue-router'
import AuthView from '@/views/AuthView.vue'

const router = useRouter()
const isAuthenticated = ref(false)

onMounted(() => {
  const token = localStorage.getItem('access_token')
  if (token) {
    isAuthenticated.value = true
    if (router.currentRoute.value.path === '/login') {
      router.replace('/home')
    }
  }
})

const handleLoginSuccess = () => {
  isAuthenticated.value = true
  router.replace('/home')
}

const handleLogout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  isAuthenticated.value = false
  router.replace('/login')
}
</script>

<template>
  <AuthView
    v-if="!isAuthenticated"
    @login-success="handleLoginSuccess"
  />

  <RouterView v-else v-slot="{ Component }">
    <component :is="Component" @logout="handleLogout" />
  </RouterView>
</template>
