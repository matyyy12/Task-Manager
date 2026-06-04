<script setup>
import { reactive } from 'vue'
import Groups from "@/api/Groups.js"

const props = defineProps({
  isOpen: Boolean
})

const emit = defineEmits(['close', 'refresh'])

const formData = reactive({
  name: '',
  description: ''
})

const resetForm = () => {
  formData.name = ''
  formData.description = ''
}

const closeForm = () => {
  resetForm()
  emit('close')
}

const submitGroup = async () => {
  try {
    await Groups.createGroup({ ...formData })

    emit('refresh')
    closeForm()
  } catch (err) {
    console.error("Błąd podczas tworzenia grupy:", err)
    alert("Wystąpił błąd podczas tworzenia grupy. Sprawdź konsolę.")
  }
}
</script>

<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
    <div class="bg-[#111622] border border-white/10 rounded-2xl w-full max-w-md shadow-2xl overflow-hidden flex flex-col animate-fade-in-up">

      <div class="px-6 py-5 border-b border-white/5 flex justify-between items-center bg-[#0d1117]/50">
        <h2 class="text-lg font-bold text-white tracking-wide">Create new group</h2>
        <button @click="closeForm" class="text-slate-500 hover:text-white transition-colors text-xl leading-none">&times;</button>
      </div>

      <form @submit.prevent="submitGroup" class="p-6 flex flex-col gap-5">
        <div>
          <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2">Group Name <span class="text-indigo-500">*</span></label>
          <input v-model="formData.name" type="text" required placeholder="e.g. Marketing Team"
            class="w-full bg-[#080b12] border border-white/10 rounded-xl px-4 py-3 text-sm text-slate-200 placeholder:text-slate-600 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all" />
        </div>

        <div>
          <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2">Description</label>
          <textarea v-model="formData.description" rows="4" placeholder="What is the purpose of this group?"
            class="w-full bg-[#080b12] border border-white/10 rounded-xl px-4 py-3 text-sm text-slate-200 placeholder:text-slate-600 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all resize-none"></textarea>
        </div>

        <div class="mt-2 pt-5 border-t border-white/5 flex justify-end gap-3">
          <button type="button" @click="closeForm" class="px-5 py-2.5 rounded-xl text-sm font-bold text-slate-400 hover:text-white hover:bg-white/5 transition-all">
            Cancel
          </button>
          <button type="submit" class="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-2.5 rounded-xl text-sm font-bold transition-all shadow-lg shadow-indigo-500/20 active:scale-95">
            Create Group
          </button>
        </div>
      </form>

    </div>
  </div>
</template>
