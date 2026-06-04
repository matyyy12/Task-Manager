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
  <div class="min-h-screen bg-[#080b12] text-slate-200 font-sans selection:bg-indigo-500/30">
    <div class="min-h-screen flex items-center justify-center px-5 py-10 sm:px-8">
      <main class="w-full max-w-[440px]">
        <div class="mb-10 flex items-center justify-center gap-3">
          <div class="h-11 w-11 rounded-xl bg-indigo-600 flex items-center justify-center text-xl font-black text-white shadow-lg shadow-indigo-500/20">
            ◈
          </div>
          <div>
            <p class="text-sm font-black text-white uppercase tracking-wider">Task Manager</p>
            <p class="text-xs text-slate-500">Team workspace</p>
          </div>
        </div>

          <div class="mb-8">
            <p class="text-xs font-black uppercase tracking-[0.22em] text-indigo-300 mb-3">
              {{ isLogin ? 'Sign in' : 'New workspace' }}
            </p>
            <h1 class="text-3xl font-black text-white tracking-tight">
              {{ isLogin ? 'Welcome back' : 'Create your account' }}
            </h1>
            <p class="text-sm text-slate-400 mt-3">
              {{ isLogin ? 'Access your groups, tasks, and invitations.' : 'Set up your account and start managing shared work.' }}
            </p>
          </div>

          <div class="mb-6 grid grid-cols-2 rounded-xl border border-white/10 bg-[#0d1117] p-1">
            <button
              type="button"
              @click="isLogin = true; errorMessage = ''"
              class="rounded-lg px-4 py-2.5 text-sm font-bold transition-all"
              :class="isLogin ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/20' : 'text-slate-400 hover:text-white'"
            >
              Sign in
            </button>
            <button
              type="button"
              @click="isLogin = false; errorMessage = ''"
              class="rounded-lg px-4 py-2.5 text-sm font-bold transition-all"
              :class="!isLogin ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/20' : 'text-slate-400 hover:text-white'"
            >
              Sign up
            </button>
          </div>

          <div v-if="errorMessage" class="mb-5 p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-300 text-sm flex items-center gap-3">
            <span class="h-2 w-2 rounded-full bg-red-400 shrink-0"></span>
            <span>{{ errorMessage }}</span>
          </div>

          <form @submit.prevent="handleSubmit" class="flex flex-col gap-5">
            <div>
              <label class="block text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2">Username</label>
              <input
                v-model="formData.username"
                type="text"
                required
                autocomplete="username"
                placeholder="Your username"
                class="w-full bg-[#0d1117] border border-white/10 rounded-xl px-4 py-3.5 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500/50 hover:border-white/20 transition-all"
              />
            </div>

            <div v-if="!isLogin">
              <label class="block text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2">Email Address</label>
              <input
                v-model="formData.email"
                type="email"
                required
                autocomplete="email"
                placeholder="you@example.com"
                class="w-full bg-[#0d1117] border border-white/10 rounded-xl px-4 py-3.5 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500/50 hover:border-white/20 transition-all"
              />
            </div>

            <div>
              <label class="block text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2">Password</label>
              <input
                v-model="formData.password"
                type="password"
                required
                autocomplete="current-password"
                placeholder="Enter password"
                class="w-full bg-[#0d1117] border border-white/10 rounded-xl px-4 py-3.5 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500/50 hover:border-white/20 transition-all"
              />
            </div>

            <div v-if="!isLogin">
              <label class="block text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2">Confirm Password</label>
              <input
                v-model="formData.confirmPassword"
                type="password"
                required
                autocomplete="new-password"
                placeholder="Repeat password"
                class="w-full bg-[#0d1117] border border-white/10 rounded-xl px-4 py-3.5 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500/50 hover:border-white/20 transition-all"
              />
            </div>

            <button
              type="submit"
              :disabled="isLoading"
              class="relative w-full flex justify-center items-center min-h-12 px-4 rounded-xl text-sm font-black text-white bg-indigo-600 hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/40 shadow-lg shadow-indigo-500/20 active:scale-[0.99] disabled:opacity-60 disabled:cursor-not-allowed transition-all mt-1"
            >
              <span v-if="isLoading" class="absolute left-4 w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
              {{ isLogin ? 'Sign In' : 'Create Account' }}
            </button>
          </form>

          <div class="mt-7 flex items-center justify-center gap-1.5 text-sm">
            <span class="text-slate-500">
              {{ isLogin ? "Don't have an account?" : "Already have an account?" }}
            </span>
            <button @click="toggleMode" type="button" class="text-white hover:text-indigo-300 font-bold transition-colors">
              {{ isLogin ? 'Sign up' : 'Sign in' }}
            </button>
          </div>
      </main>
    </div>
  </div>
</template>
