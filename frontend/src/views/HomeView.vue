<script setup>
import {ref, onMounted, computed} from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import TopHeader from '@/components/TopHeader.vue'
import KanbanBoard from '@/components/KanbanBoard.vue'
import GroupList from '@/components/GroupList.vue'
import AddTask from "@/components/AddTask.vue"
import Groups from "@/api/Groups.js";
import AddGroup from "@/components/AddGroup.vue";
import EditTask from "@/components/EditTask.vue";
import InviteGroup from "@/components/InviteGroup.vue";
import JoinGroup from "@/components/JoinGroup.vue";

defineEmits(['logout'])

const route = useRoute()
const router = useRouter()
const isAddTaskOpen = ref(false)
const isEditModalOpen = ref(false)
const selectedTask = ref(null)
const userGroups = ref([])

const activeView = computed(() => route.meta.activeView || 'groups')
const selectedGroupId = computed(() => {
  if (activeView.value !== 'board') return null
  const groupId = route.params.id
  return isNaN(groupId) ? groupId : Number(groupId)
})
const kanbanBoardRef = ref(null)
const totalTasks = ref(0)
const isAddGroupOpen = ref(false)
const isInviteGroupOpen = ref(false)
const isJoinGroupOpen = ref(false)
const activeSidebarTab = computed(() => activeView.value === 'board' ? 'groups' : activeView.value)


const handleChangeTab = (newTab) => {
  const routes = {
    groups: 'group-list',
    'my-tasks': 'my-tasks',
  }

  if (newTab !== 'board') {
    totalTasks.value = 0
  }

  router.push({ name: routes[newTab] || 'home' })
}

const handleOpenGroup = (groupId) => {
  router.push({ name: 'group', params: { id: groupId } })
}

const handleJoinedGroup = async (group) => {
  await fetchAllGroups()

  if (group?.id) {
    router.push({ name: 'group', params: { id: group.id } })
  }
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
    <Sidebar :active-tab="activeSidebarTab" @change-tab="handleChangeTab" @logout="$emit('logout')" />
    <main class="flex-1 flex flex-col min-w-0 bg-[#080b12] relative">
      <TopHeader
        :total-tasks="totalTasks"
        :group-name="currentGroupName"
        :show-add-task="activeView === 'board'"
        :show-add-group="activeView === 'groups'"
        :show-join-group="activeView === 'groups'"
        :show-invite-group="activeView === 'board'"
        @open-add-task="isAddTaskOpen = true"
        @open-add-group="isAddGroupOpen = true"
        @open-join-group="isJoinGroupOpen = true"
        @open-invite-group="isInviteGroupOpen = true"
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
        :show-group-name="activeView === 'my-tasks'"
        @edit-task="openEditModal"
        @update-tasks-count="totalTasks = $event"
      />

    </main>

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

      <JoinGroup
        :is-open="isJoinGroupOpen"
        @close="isJoinGroupOpen = false"
        @joined="handleJoinedGroup"
      />

      <InviteGroup
        :is-open="isInviteGroupOpen"
        :group-id="selectedGroupId"
        @close="isInviteGroupOpen = false"
      />

      <EditTask
        v-if="isEditModalOpen"
        :task="selectedTask"
        @close="closeEditModal"
        @submit="handleNew"
      />
  </div>
</template>
