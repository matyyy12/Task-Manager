<script setup>
defineProps({
  totalTasks: {
    type: Number,
    default: 0
  }
})

defineEmits(['openAddTask', 'openAddUser'])
</script>

<template>
  <header class="h-24 border-b border-white/5 flex items-center justify-between px-10 relative z-10 shrink-0">
    <div>
      <h1 class="text-3xl font-bold text-white tracking-tight leading-none">Task Manager</h1>
      <p class="text-sm text-slate-500 mt-2 font-medium">{{ totalTasks }} tasks</p>
    </div>

    <div class="flex items-center gap-4">
      <button @click="$emit('openAddUser')" class="bg-slate-800 hover:bg-slate-700 text-white px-7 py-3 rounded-xl text-sm font-bold transition-all border border-white/5 shadow-lg active:scale-95">
        + Add user
      </button>

      <button @click="$emit('openAddTask')" class="bg-indigo-600 hover:bg-indigo-500 text-white px-7 py-3 rounded-xl text-sm font-bold transition-all shadow-lg shadow-indigo-500/20 active:scale-95">
        + Add task
      </button>
    </div>
  </header>
</template>
