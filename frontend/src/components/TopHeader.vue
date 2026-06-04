<script setup>
defineProps({
  totalTasks: {
    type: Number,
    default: 0
  },
  groupName: {
    type: String,
    default: 'Task Manager'
  },
  showAddTask: {
    type: Boolean,
    default: false
  },
  showAddGroup: {
    type: Boolean,
    default: false
  },
  showJoinGroup: {
    type: Boolean,
    default: false
  },
  showInviteGroup: {
    type: Boolean,
    default: false
  }
})

defineEmits(['openAddTask', 'openAddGroup', 'openJoinGroup', 'openInviteGroup'])
</script>

<template>
  <header class="h-24 border-b border-white/5 flex items-center justify-between px-10 relative z-10 shrink-0">
    <div>
      <h1 class="text-3xl font-bold text-white tracking-tight leading-none">{{ groupName || 'Task Manager' }}</h1>
      <p v-if="groupName !== 'Task Manager' && groupName !== 'My Tasks'" class="text-sm text-slate-500 mt-2 font-medium">{{ totalTasks }} tasks</p>
    </div>

    <div class="flex items-center gap-4">

      <button
        v-if="showJoinGroup"
        @click="$emit('openJoinGroup')"
        class="bg-slate-700 hover:bg-slate-600 text-white px-7 py-3 rounded-xl text-sm font-bold transition-all active:scale-95"
      >
        Join group
      </button>

      <button
        v-if="showAddGroup"
        @click="$emit('openAddGroup')"
        class="bg-indigo-600 hover:bg-indigo-500 text-white px-7 py-3 rounded-xl text-sm font-bold transition-all shadow-lg shadow-indigo-500/20 active:scale-95"
      >
        + Add group
      </button>

      <button
        v-if="showInviteGroup"
        @click="$emit('openInviteGroup')"
        class="bg-slate-700 hover:bg-slate-600 text-white px-7 py-3 rounded-xl text-sm font-bold transition-all active:scale-95"
      >
        Invite
      </button>

      <button
        v-if="showAddTask"
        @click="$emit('openAddTask')"
        class="bg-indigo-600 hover:bg-indigo-500 text-white px-7 py-3 rounded-xl text-sm font-bold transition-all shadow-lg shadow-indigo-500/20 active:scale-95"
      >
        + Add task
      </button>

    </div>
  </header>
</template>
