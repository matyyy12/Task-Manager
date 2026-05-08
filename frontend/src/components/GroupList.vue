<script setup>
defineProps({
  groups: {
    type: Array,
    required: true,
    default: () => []
  }
})


defineEmits(['open-group'])
</script>

<template>
  <div class="p-8 w-full h-full overflow-y-auto">
    <div v-if="groups.length === 0" class="flex items-center justify-center h-64 border-2 border-dashed border-slate-800 rounded-2xl">
      <p class="text-slate-500 font-medium tracking-wide">NO GROUPS FOUND</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
      <div
        v-for="group in groups"
        :key="group.id"
        @click="$emit('open-group', group.id)"
        class="bg-[#111620] border border-slate-800 rounded-xl p-6 hover:border-slate-700 transition-all cursor-pointer flex flex-col gap-4 shadow-sm hover:shadow-md"
      >
        <div class="flex justify-between items-start">
          <h3 class="text-lg font-semibold text-slate-200">{{ group.name || 'Group name' }}</h3>
          <span class="bg-indigo-500/10 text-indigo-400 text-xs px-2 py-1 rounded-md border border-indigo-500/20">
            Group
          </span>
        </div>

        <p class="text-sm text-slate-400 flex-1">
          {{ group.description || 'No additional description for this group.' }}
        </p>

        <div class="mt-4 pt-4 border-t border-slate-800/50 text-xs text-slate-500 flex justify-between items-center">
          <span>ID: {{ group.id }}</span>
          <button @click.stop="console.log('Otwieram szczegóły...')" class="text-slate-300 hover:text-white transition-colors font-medium">
            View details &rarr;
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
