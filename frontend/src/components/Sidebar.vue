<script setup>
import { ref } from 'vue'

const sidebarItems = ref([
  { icon: '⊞', label: 'Board', active: true },
  { icon: '≡', label: 'List', active: false },
  { icon: '◷', label: 'Timeline', active: false },
  { icon: '◉', label: 'Team', active: false },
])
</script>

<template>
  <aside class="w-20 bg-[#0d1117] border-r border-white/5 flex flex-col items-center py-6 gap-6 flex-shrink-0 z-20 shadow-2xl">
    <div class="text-indigo-500 text-3xl font-bold mb-4">◈</div>
    <nav class="flex flex-col gap-4 w-full px-2">
      <div v-for="item in sidebarItems" :key="item.label"
        :class="[
          'flex flex-col items-center gap-1.5 py-3.5 px-1 text-[10px] uppercase tracking-tighter font-bold rounded-xl cursor-pointer transition-all',
          item.active ? 'text-indigo-400 bg-indigo-500/10' : 'text-slate-500 hover:text-slate-300 hover:bg-white/5'
        ]">
        <span class="text-2xl">{{ item.icon }}</span>
        {{ item.label }}
      </div>
    </nav>
  </aside>
</template>
