<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Groups from "@/api/Groups.js"

const route = useRoute()
const router = useRouter()

const status = ref('loading')
const message = ref('Joining group...')

const goHome = () => {
  router.replace({ name: 'home' })
}

const acceptInvitation = async () => {
  const token = route.params.token

  if (!token) {
    status.value = 'error'
    message.value = 'Invalid invitation link.'
    return
  }

  status.value = 'loading'
  message.value = 'Joining group...'

  try {
    const response = await Groups.joinByInvitation(token)
    const groupId = response.data?.id

    if (groupId) {
      router.replace({ name: 'group', params: { id: groupId } })
      return
    }

    status.value = 'success'
    message.value = 'You joined the group.'
  } catch (err) {
    console.error("Błąd podczas akceptowania zaproszenia:", err)
    status.value = 'error'
    message.value = err.response?.data?.detail || 'Could not join this group.'
  }
}

onMounted(() => {
  acceptInvitation()
})
</script>

<template>
  <div class="min-h-screen bg-[#080b12] text-slate-200 flex items-center justify-center p-6 font-sans">
    <div class="w-full max-w-md rounded-2xl border border-white/10 bg-[#111622] shadow-2xl overflow-hidden">
      <div class="px-6 py-5 border-b border-white/5 bg-[#0d1117]/50">
        <h1 class="text-lg font-bold text-white tracking-wide">Group invitation</h1>
      </div>

      <div class="p-6 flex flex-col gap-5">
        <div class="flex items-center gap-3">
          <span
            class="h-2.5 w-2.5 rounded-full"
            :class="status === 'error' ? 'bg-red-400' : status === 'success' ? 'bg-emerald-400' : 'bg-indigo-400 animate-pulse'"
          ></span>
          <p class="text-sm text-slate-300">{{ message }}</p>
        </div>

        <div v-if="status !== 'loading'" class="pt-5 border-t border-white/5 flex justify-end">
          <button
            type="button"
            @click="goHome"
            class="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-2.5 rounded-xl text-sm font-bold transition-all shadow-lg shadow-indigo-500/20 active:scale-95"
          >
            Go Home
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
