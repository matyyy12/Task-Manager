<script setup>
defineProps({
  task: {
    type: Object,
    required: true
  },
  showGroupName: {
    type: Boolean,
    default: false
  }
})
defineEmits(['edit-task'])
</script>


<template>
  <div class="group bg-[#111622]/90 border border-white/5 p-5 rounded-xl hover:border-indigo-500/30 transition-all cursor-pointer shadow-sm hover:shadow-xl hover:shadow-indigo-500/5 flex flex-col gap-4 relative">

    <button
      @click.stop="$emit('edit-task', task)"
      class="absolute top-4 right-4 opacity-0 group-hover:opacity-100 p-2 bg-white/5 hover:bg-white/10 rounded-lg text-slate-400 hover:text-indigo-400 transition-all"
      title="Edit Task"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
      </svg>
    </button>

    <h3 class="text-[16px] font-bold text-slate-100 leading-tight group-hover:text-indigo-400 transition-colors pr-8">
      {{ task.title }}
    </h3>

    <div v-if="showGroupName && task.group_name" class="inline-flex max-w-full">
      <span class="max-w-full truncate rounded-lg border border-indigo-400/20 bg-indigo-400/10 px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider text-indigo-300">
        {{ task.group_name }}
      </span>
    </div>

    <p v-if="task.description" class="text-xs text-slate-400 line-clamp-3 leading-relaxed border-l-2 border-indigo-500/20 pl-3">
      {{ task.description }}
    </p>

    <div class="mt-2 grid grid-cols-2 gap-4 pt-4 border-t border-white/5">
      <div class="flex flex-col gap-1">
        <span class="text-[9px] uppercase tracking-widest text-slate-500 font-black">Assignee</span>
        <span class="text-[11px] text-slate-300 font-medium truncate">
          {{ task.assigned_to_details?.username || 'Unassigned' }}
        </span>
      </div>

      <div class="flex flex-col gap-1">
        <span class="text-[9px] uppercase tracking-widest text-slate-500 font-black">Due Date</span>
        <span class="text-[11px] text-slate-300 font-medium">
          {{ task.due_to || 'No date' }}
        </span>
      </div>
    </div>
  </div>
</template>
