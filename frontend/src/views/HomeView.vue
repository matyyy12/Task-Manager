<script setup>
import {ref, onMounted, computed, watch} from 'vue'
import Sidebar from '@/components/Sidebar.vue'
import TopHeader from '@/components/TopHeader.vue'
import KanbanBoard from '@/components/KanbanBoard.vue'
import AddTask from "@/components/AddTask.vue"
import Task from "@/api/Task.js";
import EditTask from "@/components/EditTask.vue";
import AddUser from "@/components/AddUser.vue";
import UserList from "@/components/UserList.vue";

const isAddTaskOpen = ref(false)
const isAddUserOpen = ref(false)
const isEditModalOpen = ref(false)
const selectedTask = ref(null)
const activeView = ref(localStorage.getItem('activeTab') || 'board')
const usersListKey = ref(0)


const kanbanCols = ref([
  { id: 'todo', title: 'To Do', color: '#6b7280', tasks: [] },
  { id: 'inprogress', title: 'In Progress', color: '#f59e0b', tasks: [] },
  { id: 'done', title: 'Done', color: '#10b981', tasks: [] }
])

const fetchAllData = async () => {
  try {
    const response = await Task.getAllTasks()
    const allTasks = response.data

    kanbanCols.value.forEach(col => col.tasks = [])

    allTasks.forEach(task => {
      const formattedTask = {
        ...task,
        tag: task.category || 'General',
        tagClass: getCategoryStyle(task.category),
        avatar: task.assigned_to?.[0] || '?',
        avatarColor: '#5659ec'
      }

      if (task.completed) {
        kanbanCols.value[2].tasks.push(formattedTask)
      } else {
        if (task.category == "TODO"){
          kanbanCols.value[0].tasks.push(formattedTask)
        }
        else{
          kanbanCols.value[1].tasks.push(formattedTask)
        }
      }
      usersListKey.value++
    })
  } catch (err) {
    console.error(err)
  }
}

const totalTasks = computed(() => {
  return kanbanCols.value.reduce((total, col) => total + col.tasks.length, 0)
})

const getCategoryStyle = (catId) => {
  const styles = {
    1: 'bg-blue-400/10 text-blue-400 border border-blue-400/20',
    2: 'bg-emerald-400/10 text-emerald-400 border border-emerald-400/20',
    3: 'bg-violet-400/10 text-violet-400 border border-violet-400/20',
  }
  return styles[catId] || 'bg-slate-400/10 text-slate-400 border border-slate-400/20'
}

watch(activeView, (newTab) => {
  localStorage.setItem('activeTab', newTab)
})

onMounted(() => {
  fetchAllData()
})

const handleNew = async () => {
  try {
    await fetchAllData()
  } catch (err) {
    console.error(err)
  }
}

const openEditModal = (task) => {
  selectedTask.value = task
  isEditModalOpen.value = true
}

const closeEditModal = () => {
  isEditModalOpen.value = false
  selectedTask.value = null
}
</script>

<template>
  <div class="h-screen w-full bg-[#080b12] text-slate-200 overflow-hidden font-sans flex select-none">
    <Sidebar :active-tab="activeView" @change-tab="activeView = $event"/>
    <main class="flex-1 flex flex-col min-w-0 bg-[#080b12] relative">
      <TopHeader :total-tasks="totalTasks" @open-add-user="isAddUserOpen = true" @open-add-task="isAddTaskOpen = true "/>
      <KanbanBoard v-if="activeView === 'board'" :columns="kanbanCols" @edit-task="openEditModal" @refresh-data="fetchAllData"/>
      <UserList v-if="activeView === 'users'" :refresh-signal="usersListKey" @refresh="fetchAllData"/>
    </main>
    <AddTask :is-open="isAddTaskOpen" @close="isAddTaskOpen = false" @submit="handleNew"
             @refresh = "handleNew"/>

    <AddUser :is-open="isAddUserOpen" @close="isAddUserOpen = false" @refresh="handleNew"/>

    <EditTask
      v-if="isEditModalOpen"
      :task="selectedTask"
      @close="closeEditModal"
      @submit="fetchAllData"
    />
  </div>
</template>
