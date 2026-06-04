<script setup>
import { computed, ref, watch } from 'vue'
import Groups from "@/api/Groups.js"

const props = defineProps({
  isOpen: Boolean,
  groupId: {
    type: [Number, String, null],
    default: null
  }
})

const emit = defineEmits(['close'])

const inviteLink = ref('')
const isLoading = ref(false)
const errorMessage = ref('')
const copyMessage = ref('')

const canGenerate = computed(() => props.isOpen && props.groupId)

const buildInviteLink = (token) => {
  return `${window.location.origin}/group/invitation/${token}`
}

const generateInvitation = async () => {
  if (!canGenerate.value) return

  isLoading.value = true
  errorMessage.value = ''
  copyMessage.value = ''

  try {
    const response = await Groups.createInvitation(props.groupId)
    inviteLink.value = buildInviteLink(response.data.token)
  } catch (err) {
    console.error("Błąd podczas generowania zaproszenia:", err)
    errorMessage.value = "Nie udało się wygenerować zaproszenia."
  } finally {
    isLoading.value = false
  }
}

const closeModal = () => {
  inviteLink.value = ''
  errorMessage.value = ''
  copyMessage.value = ''
  emit('close')
}

const copyInviteLink = async () => {
  if (!inviteLink.value) return

  try {
    await navigator.clipboard.writeText(inviteLink.value)
    copyMessage.value = 'Link copied'
  } catch (err) {
    console.error("Błąd podczas kopiowania linku:", err)
    copyMessage.value = 'Copy failed'
  }
}

watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    generateInvitation()
  }
})
</script>

<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
    <div class="bg-[#111622] border border-white/10 rounded-2xl w-full max-w-md shadow-2xl overflow-hidden flex flex-col animate-fade-in-up">
      <div class="px-6 py-5 border-b border-white/5 flex justify-between items-center bg-[#0d1117]/50">
        <h2 class="text-lg font-bold text-white tracking-wide">Invite to group</h2>
        <button @click="closeModal" class="text-slate-500 hover:text-white transition-colors text-xl leading-none">&times;</button>
      </div>

      <div class="p-6 flex flex-col gap-5">
        <div>
          <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2">Invitation Link</label>
          <div class="flex gap-3">
            <input
              :value="isLoading ? 'Generating invitation...' : inviteLink"
              readonly
              class="w-full min-w-0 bg-[#080b12] border border-white/10 rounded-xl px-4 py-3 text-sm text-slate-200 placeholder:text-slate-600 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
            />
            <button
              type="button"
              :disabled="!inviteLink"
              @click="copyInviteLink"
              class="px-5 py-3 rounded-xl text-sm font-bold text-white bg-slate-700 hover:bg-slate-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              Copy
            </button>
          </div>
        </div>

        <p v-if="errorMessage" class="text-sm text-red-400">{{ errorMessage }}</p>
        <p v-if="copyMessage" class="text-sm text-emerald-400">{{ copyMessage }}</p>

        <div class="mt-2 pt-5 border-t border-white/5 flex justify-end gap-3">
          <button type="button" @click="closeModal" class="px-5 py-2.5 rounded-xl text-sm font-bold text-slate-400 hover:text-white hover:bg-white/5 transition-all">
            Close
          </button>
          <button type="button" @click="generateInvitation" :disabled="isLoading" class="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-2.5 rounded-xl text-sm font-bold transition-all shadow-lg shadow-indigo-500/20 active:scale-95 disabled:opacity-50">
            Generate New
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
