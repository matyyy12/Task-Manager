<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import Task from "@/api/Task.js";
import Groups from "@/api/Groups.js";

const props = defineProps({
  task: { type: Object, required: true }
})
const emit = defineEmits(['close', 'submit'])

const users = ref([])
const isAssigneeOpen = ref(false)

const categories = ref([
  { "id": "TODO", "name": "To Do" },
  { "id": "IN_PROGRESS", "name": "In progress" },
  { "id": "DONE", "name": "Done" }
])

const formData = reactive({
  id: props.task.id,
  title: props.task.title,
  description: props.task.description,
  due_to: props.task.due_to,
  completed: props.task.completed,
  assigned_to: props.task.assigned_to_details?.id || props.task.assigned_to,
  category: props.task.category
})

watch(() => formData.category, (newCategory) => {
  if (newCategory === 'DONE') {
    formData.completed = true
  } else if (formData.completed) {
    formData.completed = false
  }
})

watch(() => formData.completed, (isCompleted) => {
  if (isCompleted) {
    if (formData.category !== 'DONE') {
      formData.category = 'DONE'
    }
  } else {
    if (formData.category === 'DONE') {
      formData.category = 'TODO'
    }
  }
})

onMounted(async () => {
  if (!props.task?.group) return;

  try {
    const response = await Groups.getDetails(props.task.group)
    users.value = response.data.members_details || []
  } catch (err) {
    console.error(err)
    users.value = []
  }
})

const submitTask = async () => {
  try {
    await Task.updateTask({ ...formData }, props.task.id)
    emit('submit')
    emit('close')
  } catch (err) {
    console.error(err)
  }
}

const deleteTask = async () => {
  if (confirm("Are you sure you want to delete this task? This action cannot be undone.")) {
    try {
      await Task.deleteTask(props.task.id)
      emit('submit')
      emit('close')
    } catch (err) {
      console.error(err)
    }
  }
}
</script>

<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
    <div class="bg-[#111622] border border-white/10 rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden flex flex-col animate-fade-in-up">

      <div class="px-6 py-5 border-b border-white/5 flex justify-between items-center bg-[#0d1117]/50">
        <h2 class="text-lg font-bold text-white tracking-wide">Edit task</h2>
        <button @click="$emit('close')" class="text-slate-500 hover:text-white transition-colors text-xl leading-none">&times;</button>
      </div>

      <form @submit.prevent="submitTask" class="p-6 flex flex-col gap-5">
        <div>
          <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2">Title</label>
          <input v-model="formData.title" type="text" required
            class="w-full bg-[#080b12] border border-white/10 rounded-xl px-4 py-3 text-sm text-slate-200 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all" />
        </div>

        <div>
          <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2">Description</label>
          <textarea v-model="formData.description" rows="3"
            class="w-full bg-[#080b12] border border-white/10 rounded-xl px-4 py-3 text-sm text-slate-200 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all resize-none"></textarea>
        </div>

        <div class="flex gap-5">
          <div class="flex-1">
            <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2">Due Date</label>
            <input v-model="formData.due_to" type="date" required
              class="w-full bg-[#080b12] border border-white/10 rounded-xl px-4 py-3 text-sm text-slate-200 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all [color-scheme:dark]" />
          </div>

         <div class="flex-1 relative">
            <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2">Assignee *</label>
            <div @click="isAssigneeOpen = !isAssigneeOpen"
                 class="w-full bg-[#080b12] border border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all cursor-pointer flex items-center justify-between"
                 :class="formData.assigned_to ? 'text-slate-200' : 'text-slate-500'">
              <span class="truncate pr-2">
                {{ users?.find(u => u.id === formData.assigned_to)?.username || 'Select user...' }}
              </span>
              <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-slate-500 transition-transform duration-200 shrink-0" :class="{'rotate-180': isAssigneeOpen}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
            <div v-if="isAssigneeOpen" @click="isAssigneeOpen = false" class="fixed inset-0 z-40"></div>
            <div v-if="isAssigneeOpen"
                 class="absolute z-50 w-full mt-2 bg-[#1a2130] border border-white/10 rounded-xl shadow-2xl max-h-48 overflow-y-auto py-1
                        [&::-webkit-scrollbar]:w-1.5 [&::-webkit-scrollbar-track]:bg-transparent [&::-webkit-scrollbar-thumb]:bg-white/10 [&::-webkit-scrollbar-thumb]:rounded-full">
              <div v-for="user in (users || [])" :key="user.id"
                   @click="formData.assigned_to = user.id; isAssigneeOpen = false"
                   class="px-4 py-2.5 text-sm cursor-pointer transition-colors flex items-center gap-2"
                   :class="formData.assigned_to === user.id ? 'bg-indigo-600/20 text-indigo-400 font-bold' : 'text-slate-200 hover:bg-white/5'">
                <span class="w-4 flex justify-center">
                  <span v-if="formData.assigned_to === user.id">✓</span>
                </span>
                {{ user.username }}
              </div>
            </div>
          </div>
        </div>

        <div class="flex items-end gap-5">
         <div class="flex-1">
            <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2">Category</label>
            <div class="relative">
              <select v-model="formData.category"
                class="w-full bg-[#080b12] border border-white/10 rounded-xl px-4 py-3 text-sm text-slate-200 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all appearance-none cursor-pointer pr-10">
                <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
              </select>
              <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-slate-500">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>
          </div>

          <div class="flex-1 pb-3 pl-2">
            <label class="flex items-center gap-3 cursor-pointer group">
              <div class="relative flex items-center justify-center w-5 h-5 rounded border border-white/20 bg-[#080b12] group-hover:border-indigo-500 transition-colors">
                <input v-model="formData.completed" type="checkbox" class="peer sr-only" />
                <span class="opacity-0 peer-checked:opacity-100 text-indigo-400 text-xs font-bold transition-opacity">✓</span>
              </div>
              <span class="text-sm text-slate-300 font-medium select-none">Mark as completed</span>
            </label>
          </div>
        </div>

        <div class="mt-4 pt-5 border-t border-white/5 flex justify-between items-center">

          <button
            type="button"
            @click="deleteTask"
            class="text-sm font-bold text-red-500 hover:text-red-400 hover:underline transition-all flex items-center gap-2"
            title="Delete this task"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Delete Task
          </button>

          <div class="flex gap-3">
            <button type="button" @click="$emit('close')" class="px-5 py-2.5 rounded-xl text-sm font-bold text-slate-400 hover:text-white transition-all">
              Cancel
            </button>
            <button type="submit" class="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-2.5 rounded-xl text-sm font-bold shadow-lg shadow-indigo-500/20 active:scale-95 transition-all">
              Save Changes
            </button>
          </div>

        </div>
      </form>
    </div>
  </div>
</template>
