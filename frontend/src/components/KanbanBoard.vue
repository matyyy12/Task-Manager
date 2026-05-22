<script setup>
import { ref, onMounted, watch } from 'vue';
import Task from "@/api/Task.js";
import draggableComponent from "vuedraggable";
import TaskCard from "@/components/TaskCard.vue";

const emit = defineEmits(['edit-task', 'update-tasks-count'])

const props = defineProps({
  groupId: {
    type: [String, Number, null],
    required: true
  }
})

const columns = ref([
  { id: 'todo', title: 'To Do', color: '#6b7280', tasks: [] },
  { id: 'inprogress', title: 'In Progress', color: '#f59e0b', tasks: [] },
  { id: 'done', title: 'Done', color: '#10b981', tasks: [] }
])

const getCategoryStyle = (catId) => {
  const styles = {
    1: 'bg-blue-400/10 text-blue-400 border border-blue-400/20',
    2: 'bg-emerald-400/10 text-emerald-400 border border-emerald-400/20',
    3: 'bg-violet-400/10 text-violet-400 border border-violet-400/20',
  }
  return styles[catId] || 'bg-slate-400/10 text-slate-400 border border-slate-400/20'
}

const fetchTasks = async () => {
  if (!props.groupId) return;

  try {
    const response = await Task.getAllTasks(props.groupId)
    const allTasks = response.data

    columns.value.forEach(col => col.tasks = [])
    let taskCount = 0;

    allTasks.forEach(task => {
      taskCount++;
      const formattedTask = {
        ...task,
        tag: task.category || 'General',
        tagClass: getCategoryStyle(task.category),
        avatar: task.assigned_to?.[0] || '?',
        avatarColor: '#5659ec'
      }

      if (task.completed) {
        columns.value[2].tasks.push(formattedTask)
      } else {
        if (task.category == "TODO"){
          columns.value[0].tasks.push(formattedTask)
        } else {
          columns.value[1].tasks.push(formattedTask)
        }
      }
    })
    emit('update-tasks-count', taskCount)
  } catch (err) {
    console.error('Błąd pobierania zadań:', err)
  }
}

onMounted(() => {
  fetchTasks()
})

watch(() => props.groupId, () => {
  fetchTasks()
})

const onDragChange = async (evt, columnId) => {
  if (evt.added) {
    const movedTask = evt.added.element
    let backendCategory = ""
    let isCompleted = false

    if (columnId === 'todo') {
      backendCategory = "TODO"
    } else if (columnId === 'inprogress') {
      backendCategory = "IN_PROGRESS"
    } else if (columnId === 'done') {
      backendCategory = "DONE"
      isCompleted = true
    }
    try {
      const updateData = {
        category: backendCategory,
        completed: isCompleted
      }
      await Task.updateTask(updateData, movedTask.id)
      await fetchTasks()
    } catch (err) {
      console.error(err)
    }
  }
}

defineExpose({
  fetchTasks
})
</script>

<template>
  <section class="flex-1 overflow-x-auto p-10 relative z-10
    [&::-webkit-scrollbar]:h-1.5
    [&::-webkit-scrollbar-track]:bg-transparent
    [&::-webkit-scrollbar-thumb]:bg-white/5
    [&::-webkit-scrollbar-thumb]:rounded-full">

    <div class="flex gap-8 h-full min-w-max">
      <div v-for="col in columns" :key="col.id" class="w-[350px] flex flex-col gap-6 shrink-0 relative">

        <div class="flex items-center justify-between px-2">
          <div class="flex items-center gap-3">
            <span class="w-2.5 h-2.5 rounded-full shadow-[0_0_8px_rgba(255,255,255,0.1)]" :style="{ backgroundColor: col.color }"></span>
            <h2 class="text-xs font-black text-slate-300 uppercase tracking-[0.15em]">{{ col.title }}</h2>
            <span class="bg-white/5 text-slate-500 text-[10px] px-2 py-0.5 rounded-md font-black">{{ col.tasks.length }}</span>
          </div>
        </div>

        <draggableComponent
          v-model="col.tasks"
          group="tasks"
          item-key="id"
          :animation="200"
          ghost-class="opacity-20"
          @change="onDragChange($event, col.id)"
          class="flex-1 flex flex-col gap-4 overflow-y-auto pr-2 pb-20
            [&::-webkit-scrollbar]:w-1
            [&::-webkit-scrollbar-track]:bg-transparent
            [&::-webkit-scrollbar-thumb]:bg-white/10
            [&::-webkit-scrollbar-thumb]:rounded-full"
        >
          <template #item="{ element }">
            <TaskCard
              :task="element"
              @edit-task="$emit('edit-task', $event)"
            />
          </template>
        </draggableComponent>

        <div v-if="col.tasks.length === 0" class="absolute top-[80px] left-0 w-full h-24 border-2 border-dashed border-white/5 rounded-xl flex items-center justify-center text-slate-600 text-[10px] font-black uppercase tracking-widest -z-10">
          No Tasks
        </div>

      </div>
    </div>
  </section>
</template>
