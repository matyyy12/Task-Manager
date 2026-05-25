<script setup>
import {ref, onMounted, watch, computed} from 'vue'
import Sidebar from '@/components/Sidebar.vue'
import TopHeader from '@/components/TopHeader.vue'
import KanbanBoard from '@/components/KanbanBoard.vue'
import GroupList from '@/components/GroupList.vue'
import AddTask from "@/components/AddTask.vue"
import Groups from "@/api/Groups.js";
import AddGroup from "@/components/AddGroup.vue";
import EditTask from "@/components/EditTask.vue";
import UserList from "@/components/UserList.vue";

const isAddTaskOpen = ref(false)
const isAddUserOpen = ref(false)
const isEditModalOpen = ref(false)
const selectedTask = ref(null)
const activeView = ref(localStorage.getItem('activeTab') || 'groups')
const usersListKey = ref(0)
const userGroups = ref([])

const getInitialGroupId = () => {
  if (activeView.value !== 'board') return null
  const saved = localStorage.getItem('selectedGroupId')
  if (!saved) return null
  return isNaN(saved) ? saved : Number(saved)
}

const selectedGroupId = ref(getInitialGroupId())
const kanbanBoardRef = ref(null)
const totalTasks = ref(0)
const isAddGroupOpen = ref(false)


const handleChangeTab = (newTab) => {
  activeView.value = newTab
  localStorage.setItem('activeTab', newTab)
  selectedGroupId.value = null
  localStorage.removeItem('selectedGroupId')
  if (newTab !== 'board') {
    totalTasks.value = 0
  }
}

const handleOpenGroup = (groupId) => {
  selectedGroupId.value = groupId
  localStorage.setItem('selectedGroupId', groupId)
  activeView.value = 'board'
  localStorage.setItem('activeTab', 'board')
}



const fetchAllGroups = async () => {
  try {
    const response = await Groups.getAll()
    userGroups.value = response.data
  } catch (err) {
    console.error('Błąd pobierania grup:', err)
  }
}

const currentGroupName = computed(() => {
  if (activeView.value === 'my-tasks') {
    return 'My Tasks'
  }

  if (activeView.value !== 'board' || !selectedGroupId.value) {
    return 'Task Manager'
  }
  const group = userGroups.value.find(g => g.id === selectedGroupId.value)
  return group ? group.name : 'Task Manager'
})

onMounted(() => {
  fetchAllGroups()
})

const handleNew = async () => {
  try {
    if (kanbanBoardRef.value) {
      await kanbanBoardRef.value.fetchTasks()
    }
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
    <Sidebar :active-tab="activeView" @change-tab="handleChangeTab" />
    <main class="flex-1 flex flex-col min-w-0 bg-[#080b12] relative">
      <TopHeader
        :total-tasks="totalTasks"
        :group-name="currentGroupName"
        :show-add-task="activeView === 'board'"
        :show-add-group="activeView === 'groups'"
        @open-add-task="isAddTaskOpen = true"
        @open-add-group="isAddGroupOpen = true"
      />

      <GroupList
        v-if="activeView === 'groups'"
        :groups="userGroups"
        @open-group="handleOpenGroup"
      />

      <KanbanBoard
        v-if="activeView === 'board' || activeView === 'my-tasks'"
        ref="kanbanBoardRef"
        :group-id="activeView === 'my-tasks' ? null : selectedGroupId"
        @edit-task="openEditModal"
        @update-tasks-count="totalTasks = $event"
      />

      <UserList v-if="activeView === 'users'" :refresh-signal="usersListKey" @refresh="handleNew"/>    </main>

      <AddTask
        :is-open="isAddTaskOpen"
        :group-id="selectedGroupId"
        @close="isAddTaskOpen = false"
        @submit="handleNew"
        @refresh="handleNew"
      />

      <AddGroup
        :is-open="isAddGroupOpen"
        @close="isAddGroupOpen = false"
        @refresh="fetchAllGroups"
      />

      <EditTask
        v-if="isEditModalOpen"
        :task="selectedTask"
        @close="closeEditModal"
        @submit="handleNew"
      />
  </div>
</template>
