<script setup>
defineEmits(['openAddTask'])
</script>


<template>
  <header class="h-24 border-b border-white/5 flex items-center justify-between px-10 relative z-10 shrink-0">
    <div>
      <h1 class="text-3xl font-bold text-white tracking-tight leading-none">Sprint #4</h1>
      <p class="text-sm text-slate-500 mt-2 font-medium">14 tasks • Due Apr 30</p>
    </div>

    <div class="flex items-center gap-8">
      <div class="flex -space-x-3">
        <div class="w-10 h-10 rounded-full border-2 border-[#080b12] bg-blue-500 flex items-center justify-center text-xs font-bold text-white shadow-lg">K</div>
        <div class="w-10 h-10 rounded-full border-2 border-[#080b12] bg-emerald-500 flex items-center justify-center text-xs font-bold text-white shadow-lg">J</div>
        <div class="w-10 h-10 rounded-full border-2 border-[#080b12] bg-rose-500 flex items-center justify-center text-xs font-bold text-white shadow-lg">M</div>
      </div>
      <button @click="$emit('openAddTask')" class="bg-indigo-600 hover:bg-indigo-500 text-white px-7 py-3 rounded-xl text-sm font-bold transition-all shadow-lg shadow-indigo-500/20 active:scale-95">
        + Add task
      </button>
    </div>
  </header>
</template>
