<script setup>
import { ref, reactive } from 'vue'
import Token from "@/api/Token.js";
const emit = defineEmits(['login-success'])

const isLogin = ref(true)
const isLoading = ref(false)
const errorMessage = ref('')

const formData = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  email: ''
})

const toggleMode = () => {
  isLogin.value = !isLogin.value
  errorMessage.value = ''
  formData.password = ''
  formData.confirmPassword = ''
}

const handleSubmit = async () => {
  isLoading.value = true
  errorMessage.value = ''

  if (!isLogin.value && formData.password !== formData.confirmPassword) {
    errorMessage.value = "Passwords do not match."
    isLoading.value = false
    return
  }

  try {
    let response;

    if (isLogin.value) {
      response = await Token.login({
        username: formData.username,
        password: formData.password
      })
    } else {
      response = await Token.register({
        username: formData.username,
        email: formData.email,
        password: formData.password
      })
    }

    const { access_token, refresh_token } = response.data
    localStorage.setItem('access_token', access_token)
    localStorage.setItem('refresh_token', refresh_token)

    emit('login-success')

  } catch (err) {
    console.error("Błąd autoryzacji:", err)
    errorMessage.value = err.response?.data?.detail || "Invalid credentials. Please try again."
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-[#030712] p-4 relative overflow-hidden font-sans selection:bg-indigo-500/30">

    <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-indigo-600/20 rounded-full mix-blend-screen filter blur-[100px] animate-pulse"></div>
    <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-600/10 rounded-full mix-blend-screen filter blur-[100px] animate-pulse" style="animation-delay: 2s;"></div>

    <div class="w-full max-w-[420px] bg-white/[0.03] backdrop-blur-2xl border border-white/10 rounded-[2rem] p-10 shadow-2xl relative z-10">

      <div class="text-center mb-10 flex flex-col items-center">
        <div class="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl mb-6 flex items-center justify-center shadow-lg shadow-indigo-500/25 ring-1 ring-white/20">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10l-2 1m0 0l-2-1m2 1v2.5M20 7l-2 1m2-1l-2-1m2 1v2.5M14 4l-2-1-2 1M4 7l2-1M4 7l2 1M4 7v2.5M12 21l-2-1m2 1l2-1m-2 1v-2.5M6 18l-2-1v-2.5M18 18l2-1v-2.5" />
          </svg>
        </div>

        <h1 class="text-3xl font-bold text-white tracking-tight mb-2">
          {{ isLogin ? 'Welcome back' : 'Create account' }}
        </h1>
        <p class="text-slate-400 text-sm">
          {{ isLogin ? 'Enter your details to access your workspace.' : 'Start managing your team today.' }}
        </p>
      </div>

      <div v-if="errorMessage" class="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 text-sm text-center flex items-center justify-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 shrink-0" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
        {{ errorMessage }}
      </div>

      <form @submit.prevent="handleSubmit" class="flex flex-col gap-7">

        <div>
          <label class="block text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2 pl-1">Username</label>
          <input v-model="formData.username" type="text" required
            class="w-full bg-black/20 border border-white/5 rounded-xl px-4 py-3.5 text-sm text-white focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500/50 hover:border-white/10 transition-all" />
        </div>

        <div v-if="!isLogin">
          <label class="block text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2 pl-1">Email Address</label>
          <input v-model="formData.email" type="email" required
            class="w-full bg-black/20 border border-white/5 rounded-xl px-4 py-3.5 text-sm text-white focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500/50 hover:border-white/10 transition-all" />
        </div>

        <div>
          <label class="block text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2 pl-1 flex justify-between">
            <span>Password</span>
            <a v-if="isLogin" href="#" class="text-indigo-400 hover:text-indigo-300 normal-case tracking-normal">Forgot?</a>
          </label>
          <input v-model="formData.password" type="password" required
            class="w-full bg-black/20 border border-white/5 rounded-xl px-4 py-3.5 text-sm text-white focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500/50 hover:border-white/10 transition-all" />
        </div>

        <div v-if="!isLogin">
          <label class="block text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2 pl-1">Confirm Password</label>
          <input v-model="formData.confirmPassword" type="password" required
            class="w-full bg-black/20 border border-white/5 rounded-xl px-4 py-3.5 text-sm text-white focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500/50 hover:border-white/10 transition-all" />
        </div>

        <button type="submit" :disabled="isLoading"
          class="group relative w-full flex justify-center py-3.5 px-4 border border-transparent rounded-xl text-sm font-bold text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-[#030712] focus:ring-indigo-500 shadow-lg shadow-indigo-500/25 active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed transition-all mt-2">
          <span v-if="isLoading" class="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
          {{ isLogin ? 'Sign In' : 'Create Account' }}
        </button>

      </form>

      <div class="mt-8 text-center text-sm">
        <span class="text-slate-500">
          {{ isLogin ? "Don't have an account?" : "Already have an account?" }}
        </span>
        <button @click="toggleMode" type="button" class="text-white hover:text-indigo-400 font-bold ml-1.5 transition-colors">
          {{ isLogin ? 'Sign up' : 'Sign in' }}
        </button>
      </div>

    </div>
  </div>
</template>
