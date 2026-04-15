<script setup>
import { ref, reactive, onMounted, watch} from 'vue'
import User from "@/api/User.js";
import Task from "@/api/Task.js";

const props = defineProps({
  task: { type: Object, required: true }
})

const emit = defineEmits(['close', 'submit'])

const users = ref([])
const categories = ref([{"id": "TODO","name": "To Do"},
                              {"id": "IN_PROGRESS","name": "In progress"},
                              {"id": "DONE","name": "Done"}])

const formData = reactive({
  title: props.task.title,
  description: props.task.description,
  due_to: props.task.due_to,
  completed: props.task.completed,
  assigned_to: props.task.assigned_to_details?.id || props.task.assigned_to,
  category: props.task.category
})


const updateTask = async () => {
  try{
    await Task.updateTask(formData, props.task.id)
    emit('submit')
    emit('close')
  }
  catch (err){
    console.error(err)
  }
}


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
  try {
    const usersResponse = await User.getAllUsers()
    users.value = usersResponse.data
  } catch (err) {
    console.error("Błąd pobierania użytkowników:", err)
  }
})
</script>

<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
    <div class="bg-[#111622] border border-white/10 rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden flex flex-col animate-fade-in-up">

      <div class="px-6 py-5 border-b border-white/5 flex justify-between items-center bg-[#0d1117]/50">
        <h2 class="text-lg font-bold text-white tracking-wide">Edit task</h2>
        <button @click="$emit('close')" class="text-slate-500 hover:text-white transition-colors text-xl leading-none">&times;</button>
      </div>

      <form @submit.prevent="updateTask" class="p-6 flex flex-col gap-5">
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

          <div class="flex-1">
            <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2">Assignee</label>
            <select v-model="formData.assigned_to" required
              class="w-full bg-[#080b12] border border-white/10 rounded-xl px-4 py-3 text-sm text-slate-200 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all appearance-none cursor-pointer">
              <option value="" disabled>Select user...</option>
              <option v-for="user in users" :key="user.id" :value="user.id">{{ user.username }}</option>
            </select>
          </div>
        </div>

        <div class="flex items-end gap-5">
          <div class="flex-1">
            <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2">Category</label>
            <select v-model="formData.category"
              class="w-full bg-[#080b12] border border-white/10 rounded-xl px-4 py-3 text-sm text-slate-200 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all appearance-none cursor-pointer">
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
            </select>
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

        <div class="mt-4 pt-5 border-t border-white/5 flex justify-end gap-3">
          <button type="button" @click="$emit('close')" class="px-5 py-2.5 rounded-xl text-sm font-bold text-slate-400 hover:text-white transition-all">
            Cancel
          </button>
          <button type="submit" @click="updateTask" class="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-2.5 rounded-xl text-sm font-bold shadow-lg shadow-indigo-500/20 active:scale-95">
            Save Changes
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
