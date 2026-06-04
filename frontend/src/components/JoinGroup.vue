<script setup>
import { ref } from 'vue'
import Groups from "@/api/Groups.js"

defineProps({
  isOpen: Boolean
})

const emit = defineEmits(['close', 'joined'])

const invitationValue = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

const extractToken = (value) => {
  const trimmed = value.trim()
  if (!trimmed) return ''

  try {
    const url = new URL(trimmed)
    const parts = url.pathname.split('/').filter(Boolean)
    return parts[parts.length - 1] || ''
  } catch {
    const parts = trimmed.split('/').filter(Boolean)
    return parts[parts.length - 1] || trimmed
  }
}

const closeModal = () => {
  invitationValue.value = ''
  errorMessage.value = ''
  emit('close')
}

const submitJoin = async () => {
  const token = extractToken(invitationValue.value)

  if (!token) {
    errorMessage.value = 'Paste an invitation link or token.'
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  try {
    await Groups.joinByInvitation(token)
    emit('joined')
    closeModal()
  } catch (err) {
    console.error("Błąd podczas dołączania do grupy:", err)
    errorMessage.value = err.response?.data?.detail || "Nie udało się dołączyć do grupy."
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
    <div class="bg-[#111622] border border-white/10 rounded-2xl w-full max-w-md shadow-2xl overflow-hidden flex flex-col animate-fade-in-up">
      <div class="px-6 py-5 border-b border-white/5 flex justify-between items-center bg-[#0d1117]/50">
        <h2 class="text-lg font-bold text-white tracking-wide">Join group</h2>
        <button @click="closeModal" class="text-slate-500 hover:text-white transition-colors text-xl leading-none">&times;</button>
      </div>

      <form @submit.prevent="submitJoin" class="p-6 flex flex-col gap-5">
        <div>
          <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2">Invitation Link</label>
          <input
            v-model="invitationValue"
            type="text"
            required
            placeholder="Paste invitation link or token"
            class="w-full bg-[#080b12] border border-white/10 rounded-xl px-4 py-3 text-sm text-slate-200 placeholder:text-slate-600 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
          />
        </div>

        <p v-if="errorMessage" class="text-sm text-red-400">{{ errorMessage }}</p>

        <div class="mt-2 pt-5 border-t border-white/5 flex justify-end gap-3">
          <button type="button" @click="closeModal" class="px-5 py-2.5 rounded-xl text-sm font-bold text-slate-400 hover:text-white hover:bg-white/5 transition-all">
            Cancel
          </button>
          <button type="submit" :disabled="isLoading" class="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-2.5 rounded-xl text-sm font-bold transition-all shadow-lg shadow-indigo-500/20 active:scale-95 disabled:opacity-50">
            {{ isLoading ? 'Joining...' : 'Join Group' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
