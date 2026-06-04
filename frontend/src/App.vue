<script setup>
import { ref, onMounted } from 'vue'
import { RouterView, useRoute, useRouter } from 'vue-router'
import AuthView from '@/views/AuthView.vue'
import Token from "@/api/Token.js";

const route = useRoute()
const router = useRouter()
const isAuthenticated = ref(Boolean(localStorage.getItem('access_token')))

const getLoginRedirect = () => {
  const redirect = route.query.redirect
  return typeof redirect === 'string' && redirect.startsWith('/') && !redirect.startsWith('//')
    ? redirect
    : '/home'
}

onMounted(() => {
  const token = localStorage.getItem('access_token')
  if (token) {
    isAuthenticated.value = true
    if (router.currentRoute.value.path === '/login') {
      router.replace(getLoginRedirect())
    }
  }
})

const handleLoginSuccess = () => {
  isAuthenticated.value = true
  router.replace(getLoginRedirect())
}

const handleLogout = async () => {
  try {
    await Token.logout()
  } catch (err) {
    console.error("Błąd podczas wylogowania:", err)
  } finally {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    isAuthenticated.value = false
    router.replace('/login')
  }
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
