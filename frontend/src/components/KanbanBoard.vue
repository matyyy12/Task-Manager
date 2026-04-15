<script setup>
defineEmits(['edit-task'])
import TaskCard from "@/components/TaskCard.vue";
const props = defineProps({
  columns: Array
})
</script>

<template>
  <section class="flex-1 overflow-x-auto p-10 relative z-10
    [&::-webkit-scrollbar]:h-1.5
    [&::-webkit-scrollbar-track]:bg-transparent
    [&::-webkit-scrollbar-thumb]:bg-white/5
    [&::-webkit-scrollbar-thumb]:rounded-full">

    <div class="flex gap-8 h-full min-w-max">

      <div v-for="col in columns" :key="col.title" class="w-[350px] flex flex-col gap-6 shrink-0">

        <div class="flex items-center justify-between px-2">
          <div class="flex items-center gap-3">
            <span class="w-2.5 h-2.5 rounded-full shadow-[0_0_8px_rgba(255,255,255,0.1)]" :style="{ backgroundColor: col.color }"></span>
            <h2 class="text-xs font-black text-slate-300 uppercase tracking-[0.15em]">{{ col.title }}</h2>
            <span class="bg-white/5 text-slate-500 text-[10px] px-2 py-0.5 rounded-md font-black">{{ col.tasks.length }}</span>
          </div>
        </div>

        <div class="flex-1 flex flex-col gap-4 overflow-y-auto pr-2
          [&::-webkit-scrollbar]:w-1
          [&::-webkit-scrollbar-track]:bg-transparent
          [&::-webkit-scrollbar-thumb]:bg-white/10
          [&::-webkit-scrollbar-thumb]:rounded-full">

          <TaskCard
            v-for="task in col.tasks"
            :key="task.id"
            :task="task"
            @edit-task="$emit('edit-task', $event)"
          />

          <div v-if="col.tasks.length === 0" class="h-24 border-2 border-dashed border-white/5 rounded-xl flex items-center justify-center text-slate-600 text-[10px] font-black uppercase tracking-widest">
            No Tasks
          </div>

        </div>
      </div>
    </div>
  </section>
</template>
