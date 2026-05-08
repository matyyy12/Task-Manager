<script setup>
import { ref, reactive } from 'vue'
import User from "@/api/User.js";

const props = defineProps({
  user: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['refresh'])

const isEditing = ref(false)

const editData = reactive({
  username: props.user.username,
  email: props.user.email
})

const startEditing = () => {
  editData.username = props.user.username
  editData.email = props.user.email
  isEditing.value = true
}

const cancelEdit = () => {
  isEditing.value = false
}

const deleteUser = async () => {
  try{
    await User.deleteUser()
    emit('refresh')
  }
  catch (err){
    console.error(err)
  }
}

const saveUser = async () => {
  try {
    await User.updateUser(editData)
    isEditing.value = false
    emit('refresh')
  } catch (err) {
    console.error(err)
  }
}
</script>

<template>
  <div class="bg-[#111622] border border-white/5 rounded-2xl p-6 hover:border-indigo-500/30 transition-all flex flex-col gap-6 shadow-xl relative group min-h-[280px]">

    <div v-if="!isEditing" class="absolute top-4 right-4 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
      <button @click="startEditing" class="text-slate-500 hover:text-indigo-400 p-1" title="Edit User">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
        </svg>
      </button>
      <button @click="deleteUser" class="text-slate-500 hover:text-red-500 p-1" title="Delete User">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
      </button>
    </div>

    <div class="flex items-start gap-4 pr-2">
      <div class="w-12 h-12 rounded-full bg-gradient-to-tr from-indigo-600 to-purple-600 flex items-center justify-center text-white font-black shadow-lg uppercase shrink-0">
        {{ editData.username.charAt(0) }}
      </div>

      <div v-if="isEditing" class="flex-1 flex flex-col gap-2 animate-fade-in">
        <input v-model="editData.username" type="text" class="bg-[#080b12] border border-white/10 rounded-lg px-3 py-1.5 text-sm text-white focus:outline-none focus:border-indigo-500 w-full" />
        <input v-model="editData.email" type="email" class="bg-[#080b12] border border-white/10 rounded-lg px-3 py-1.5 text-xs text-slate-300 focus:outline-none focus:border-indigo-500 w-full" />

        <div class="flex items-center justify-between mt-2">
            <div class="flex gap-2">
                <button @click="saveUser" class="bg-indigo-600 hover:bg-indigo-500 text-white text-[10px] px-3 py-1.5 rounded-md font-bold transition-all uppercase tracking-wider">
                    Save
                </button>
                <button @click="cancelEdit" class="text-slate-500 hover:text-white text-[10px] px-3 py-1.5 rounded-md font-bold transition-all uppercase tracking-wider">
                    Cancel
                </button>
            </div>
            <button @click="deleteUser" class="text-red-500/60 hover:text-red-500 text-[10px] font-bold uppercase tracking-wider transition-colors">
                Delete
            </button>
        </div>
      </div>

      <div v-else class="overflow-hidden">
        <h3 class="text-white font-bold text-lg leading-tight truncate">{{ user.username }}</h3>
        <p class="text-slate-500 text-xs truncate">{{ user.email || 'No email address' }}</p>
      </div>
    </div>

    <div :class="{'opacity-20 pointer-events-none blur-[2px] scale-95': isEditing}" class="transition-all duration-500 flex flex-col gap-6 h-full origin-top">
      <div class="grid grid-cols-3 gap-2 border-t border-white/5 pt-5">
        <div class="flex flex-col items-center p-2.5 bg-[#080b12] rounded-xl border border-white/5">
          <span class="text-slate-500 text-[9px] uppercase font-bold tracking-widest mb-1">To Do</span>
          <span class="text-white font-black text-lg leading-none">{{ user.todo }}</span>
        </div>
        <div class="flex flex-col items-center p-2.5 bg-[#080b12] rounded-xl border border-white/5">
          <span class="text-orange-400 text-[9px] uppercase font-bold tracking-widest mb-1">In Prog</span>
          <span class="text-white font-black text-lg leading-none">{{ user.inProgress }}</span>
        </div>
        <div class="flex flex-col items-center p-2.5 bg-[#080b12] rounded-xl border border-white/5">
          <span class="text-emerald-400 text-[9px] uppercase font-bold tracking-widest mb-1">Done</span>
          <span class="text-white font-black text-lg leading-none">{{ user.completed }}</span>
        </div>
      </div>

      <div class="mt-auto pt-2">
        <div class="flex justify-between text-[11px] font-bold mb-2 uppercase tracking-wider">
          <span class="text-slate-500">Workload</span>
          <span class="text-indigo-400">{{ user.totalTasks }} Tasks</span>
        </div>
        <div class="w-full h-1.5 bg-[#080b12] rounded-full overflow-hidden flex shadow-inner">
          <div class="h-full bg-slate-500 transition-all duration-500" :style="{ width: user.totalTasks ? (user.todo / user.totalTasks * 100) + '%' : '0%' }"></div>
          <div class="h-full bg-orange-500 transition-all duration-500" :style="{ width: user.totalTasks ? (user.inProgress / user.totalTasks * 100) + '%' : '0%' }"></div>
          <div class="h-full bg-emerald-500 transition-all duration-500" :style="{ width: user.totalTasks ? (user.completed / user.totalTasks * 100) + '%' : '0%' }"></div>
        </div>
      </div>
    </div>
  </div>
</template>
