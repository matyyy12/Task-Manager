<script setup>
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

          <div v-for="task in col.tasks" :key="task.id"
            class="group bg-[#111622]/90 border border-white/5 p-5 rounded-xl hover:border-indigo-500/30 transition-all cursor-pointer shadow-sm hover:shadow-xl hover:shadow-indigo-500/5 flex flex-col gap-4">

            <h3 class="text-[16px] font-bold text-slate-100 leading-tight group-hover:text-indigo-400 transition-colors">
              {{ task.title }}
            </h3>

            <p v-if="task.description" class="text-xs text-slate-400 line-clamp-3 leading-relaxed border-l-2 border-indigo-500/20 pl-3">
              {{ task.description }}
            </p>

            <div class="mt-2 grid grid-cols-2 gap-4 pt-4 border-t border-white/5">
              <div class="flex flex-col gap-1">
                <span class="text-[9px] uppercase tracking-widest text-slate-500 font-black">Assignee</span>
                <span class="text-[11px] text-slate-300 font-medium truncate">
                  {{ task.assigned_to_details.username || 'User ' + task.assigned_to_details.username }}
                </span>
              </div>

              <div class="flex flex-col gap-1">
                <span class="text-[9px] uppercase tracking-widest text-slate-500 font-black">Due Date</span>
                <span class="text-[11px] text-slate-300 font-medium">
                  {{ task.due_to }}
                </span>
              </div>
            </div>

          </div>

          <div v-if="col.tasks.length === 0" class="h-24 border-2 border-dashed border-white/5 rounded-xl flex items-center justify-center text-slate-600 text-[10px] font-black uppercase tracking-widest">
            No Tasks
          </div>

        </div>
      </div>
    </div>
  </section>
</template>
