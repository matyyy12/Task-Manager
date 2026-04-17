<script setup>
import { reactive } from 'vue'
import User from "@/api/User.js"

const props = defineProps({
  isOpen: Boolean
})

const emit = defineEmits(['close', 'refresh'])

const formData = reactive({
  username: '',
  email: ''
})

const closeForm = () => {
  formData.username = ''
  formData.email = ''
  emit('close')
}

const submitUser = async () => {
  try {
    const payload = {
      username: formData.username
    }
    if (formData.email) {
      payload.email = formData.email
    }
    await User.createUser(payload)
    emit('refresh')
    closeForm()
  } catch (err) {
    console.error(err)
  }
}
</script>

<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
    <div class="bg-[#111622] border border-white/10 rounded-2xl w-full max-w-md shadow-2xl overflow-hidden flex flex-col animate-fade-in-up">

      <div class="px-6 py-5 border-b border-white/5 flex justify-between items-center bg-[#0d1117]/50">
        <h2 class="text-lg font-bold text-white tracking-wide">Add New User</h2>
        <button @click="closeForm" class="text-slate-500 hover:text-white transition-colors text-xl leading-none">&times;</button>
      </div>

      <form @submit.prevent="submitUser" class="p-6 flex flex-col gap-5">

        <div>
          <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2">
            Username <span class="text-indigo-500">*</span>
          </label>
          <input
            v-model="formData.username"
            type="text"
            required
            placeholder="e.g. jdoe"
            class="w-full bg-[#080b12] border border-white/10 rounded-xl px-4 py-3 text-sm text-slate-200 placeholder:text-slate-600 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
          />
        </div>

        <div>
          <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2">Email Address</label>
          <input
            v-model="formData.email"
            type="email"
            placeholder="e.g. john@example.com"
            class="w-full bg-[#080b12] border border-white/10 rounded-xl px-4 py-3 text-sm text-slate-200 placeholder:text-slate-600 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
          />
        </div>

        <div class="mt-4 pt-5 border-t border-white/5 flex justify-end gap-3">
          <button type="button" @click="closeForm" class="px-5 py-2.5 rounded-xl text-sm font-bold text-slate-400 hover:text-white transition-all">
            Cancel
          </button>
          <button type="submit" class="bg-indigo-600 hover:bg-indigo-500 text-white px-8 py-2.5 rounded-xl text-sm font-bold shadow-lg shadow-indigo-500/20 active:scale-95 transition-all">
            Create User
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
