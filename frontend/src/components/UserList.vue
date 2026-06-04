<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import User from "@/api/User.js"
import Task from "@/api/Task.js"
import UserCard from "@/components/UserCard.vue"

const props = defineProps({
  refreshSignal: Number
})

const emit = defineEmits(['refresh'])

const users = ref([])
const tasks = ref([])
const isLoading = ref(true)

const fetchData = async () => {
  isLoading.value = true
  try {
    const [usersRes, tasksRes] = await Promise.all([
      User.getAllUsers(),
      Task.getAll(group)
    ])
    users.value = usersRes.data
    tasks.value = tasksRes.data
  } catch (e) {
    console.error(e)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchData()
})

watch(() => props.refreshSignal, () => {
  fetchData()
})

const usersWithStats = computed(() => {
  return users.value.map(user => {
    const userTasks = tasks.value.filter(t =>
      t.assigned_to === user.id || t.assigned_to_details?.id === user.id
    )

    const completed = userTasks.filter(t => t.completed).length
    const todo = userTasks.filter(t => !t.completed && t.category === 'TODO').length
    const inProgress = userTasks.filter(t => !t.completed && t.category === 'IN_PROGRESS').length

    return {
      ...user,
      totalTasks: userTasks.length,
      completed,
      todo,
      inProgress
    }
  }).sort((a,b) => a.id - b.id)
})
</script>

<template>
  <section class="flex-1 overflow-y-auto p-10 relative z-10
    [&::-webkit-scrollbar]:w-1.5
    [&::-webkit-scrollbar-track]:bg-transparent
    [&::-webkit-scrollbar-thumb]:bg-white/5
    [&::-webkit-scrollbar-thumb]:rounded-full">

    <div class="max-w-6xl mx-auto">
      <div class="mb-8">
        <h2 class="text-2xl font-bold text-white tracking-tight">Team Members</h2>
        <p class="text-slate-500 text-sm mt-1">Manage your team and track their task progress.</p>
      </div>

      <div v-if="isLoading" class="flex justify-center items-center h-32">
        <span class="text-slate-500 font-bold animate-pulse">Loading team data...</span>
      </div>

      <div v-else class="grid grid-cols-1 xl:grid-cols-3 lg:grid-cols-2 gap-6">

        <UserCard
          v-for="user in usersWithStats"
          :key="user.id"
          :user="user"
          @refresh="fetchData(); $emit('refresh')"
        />

      </div>
    </div>
  </section>
</template>
