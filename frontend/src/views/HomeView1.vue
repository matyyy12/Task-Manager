<template>
  <div class="relative min-h-screen bg-[#080b12] text-slate-200 overflow-x-hidden font-['DM_Sans',sans-serif]">

    <!-- Animated background -->
    <div class="bg-grid"></div>
    <div class="fixed top-[-200px] left-1/2 -translate-x-1/2 w-[800px] h-[600px] bg-[radial-gradient(ellipse,rgba(99,102,241,0.15)_0%,transparent_70%)] pointer-events-none z-0"></div>

    <!-- Navigation -->
    <nav class="relative z-10 flex items-center justify-between px-15 py-5 border-b border-white/[0.06]">
      <div class="flex items-center gap-2.5 font-['Syne',sans-serif] font-bold text-xl text-white">
        <span class="text-indigo-400 text-2xl">◈</span>
        <span>TaskFlow</span>
      </div>
      <div class="flex gap-8">
        <a href="#" class="text-slate-400 text-sm no-underline hover:text-white transition-colors">Dashboard</a>
        <a href="#" class="text-slate-400 text-sm no-underline hover:text-white transition-colors">Tasks</a>
        <a href="#" class="text-slate-400 text-sm no-underline hover:text-white transition-colors">Team</a>
      </div>
      <div class="flex gap-3 items-center">
        <button class="bg-transparent border-none text-slate-400 font-['DM_Sans',sans-serif] text-sm cursor-pointer px-4 py-2 hover:text-white transition-colors">Sign in</button>
        <button class="bg-indigo-500 text-white border-none font-['DM_Sans',sans-serif] text-sm font-medium px-5 py-2.5 rounded-lg cursor-pointer hover:bg-indigo-600 hover:-translate-y-px transition-all">Get Started</button>
      </div>
    </nav>

    <!-- Hero -->
    <section class="relative z-[1] text-center px-10 pt-24 pb-15 max-w-4xl mx-auto">
      <div class="animate-fade-in-down inline-flex items-center gap-2 bg-indigo-500/[0.12] border border-indigo-500/30 text-indigo-300 text-xs px-3.5 py-1.5 rounded-full mb-8">
        <span class="animate-pulse-dot w-1.5 h-1.5 bg-indigo-400 rounded-full"></span>
        Now in beta · Built for teams
      </div>

      <h1 class="animate-fade-in-down-1 font-['Syne',sans-serif] text-[clamp(2.8rem,6vw,5rem)] font-extrabold leading-[1.1] tracking-[-0.03em] text-white mb-6">
        <span class="block">Manage work</span>
        <span class="block text-indigo-400">without the noise.</span>
      </h1>

      <p class="animate-fade-in-down-2 text-lg text-slate-500 max-w-[520px] mx-auto mb-10 leading-relaxed font-light">
        A focused task manager for teams who ship. Assign, track, and close tasks — nothing more, nothing less.
      </p>

      <div class="animate-fade-in-down-3 flex gap-3.5 justify-center mb-14">
        <button
          @click="getStarted"
          class="inline-flex items-center gap-2 bg-indigo-500 text-white border-none font-['DM_Sans',sans-serif] text-base font-medium px-8 py-3.5 rounded-[10px] cursor-pointer hover:bg-indigo-600 hover:-translate-y-px transition-all group"
        >
          Start for free
          <span class="transition-transform group-hover:translate-x-1">→</span>
        </button>
        <button class="bg-transparent text-slate-400 border border-white/[0.12] font-['DM_Sans',sans-serif] text-base font-medium px-8 py-3.5 rounded-[10px] cursor-pointer hover:border-indigo-500 hover:text-white transition-all">
          Watch demo
        </button>
      </div>

      <div class="animate-fade-in-down-4 flex items-center justify-center gap-8">
        <div class="text-center">
          <span class="block font-['Syne',sans-serif] text-2xl font-bold text-white">2.4k</span>
          <span class="text-xs text-slate-500">active users</span>
        </div>
        <div class="w-px h-8 bg-white/[0.08]"></div>
        <div class="text-center">
          <span class="block font-['Syne',sans-serif] text-2xl font-bold text-white">98%</span>
          <span class="text-xs text-slate-500">uptime</span>
        </div>
        <div class="w-px h-8 bg-white/[0.08]"></div>
        <div class="text-center">
          <span class="block font-['Syne',sans-serif] text-2xl font-bold text-white">12ms</span>
          <span class="text-xs text-slate-500">avg response</span>
        </div>
      </div>
    </section>

    <!-- Dashboard Preview -->
    <section class="animate-fade-in-up relative z-[1] px-15 pb-20">
      <div class="relative max-w-[1000px] mx-auto">
        <div class="rounded-2xl overflow-hidden border border-white/[0.08] shadow-[0_40px_120px_rgba(0,0,0,0.6)] bg-[#0f1420]">

          <!-- Top bar -->
          <div class="bg-[#161c2d] px-4 py-3 flex items-center gap-4 border-b border-white/[0.06]">
            <div class="flex gap-1.5">
              <span class="w-2.5 h-2.5 rounded-full bg-red-500"></span>
              <span class="w-2.5 h-2.5 rounded-full bg-amber-400"></span>
              <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
            </div>
            <div class="bg-white/[0.05] rounded-md px-4 py-1 text-xs text-slate-500 flex-1 max-w-[280px] text-center">
              taskflow.app/dashboard
            </div>
          </div>

          <!-- Dashboard body -->
          <div class="flex h-[420px]">

            <!-- Sidebar -->
            <div class="w-16 bg-[#0d1117] border-r border-white/[0.05] flex flex-col items-center py-4 gap-2">
              <div class="text-indigo-500 text-xl mb-4">◈</div>
              <div class="flex flex-col gap-1 w-full">
                <div v-for="item in sidebarItems" :key="item.label"
                  :class="['flex flex-col items-center gap-0.5 py-2.5 px-1 text-[0.55rem] rounded-md mx-1 cursor-pointer transition-all',
                    item.active ? 'text-indigo-400 bg-indigo-500/10' : 'text-slate-500']">
                  <span class="text-base">{{ item.icon }}</span>
                  {{ item.label }}
                </div>
              </div>
            </div>

            <!-- Main -->
            <div class="flex-1 p-5 overflow-hidden">
              <div class="flex justify-between items-start mb-5">
                <div>
                  <div class="font-['Syne',sans-serif] text-base font-bold text-white">Sprint #4</div>
                  <div class="text-[0.72rem] text-slate-500 mt-0.5">14 tasks · Due Apr 30</div>
                </div>
                <div class="flex gap-2.5 items-center">
                  <div class="bg-indigo-500 text-white text-[0.7rem] px-2.5 py-1 rounded-md cursor-pointer">+ Add task</div>
                  <div class="flex">
                    <div class="w-6 h-6 rounded-full flex items-center justify-center text-[0.65rem] font-bold text-white border-2 border-[#0f1420] bg-red-400">M</div>
                    <div class="w-6 h-6 rounded-full flex items-center justify-center text-[0.65rem] font-bold text-white border-2 border-[#0f1420] -ml-1.5 bg-blue-400">K</div>
                    <div class="w-6 h-6 rounded-full flex items-center justify-center text-[0.65rem] font-bold text-white border-2 border-[#0f1420] -ml-1.5 bg-emerald-400">J</div>
                  </div>
                </div>
              </div>

              <!-- Kanban -->
              <div class="grid grid-cols-3 gap-3 h-[calc(100%-60px)]">
                <div v-for="col in kanbanCols" :key="col.title"
                  class="bg-white/[0.02] rounded-lg p-2.5 flex flex-col gap-2">
                  <div class="flex items-center gap-1.5 text-[0.72rem] font-semibold text-slate-400 mb-1">
                    <span class="w-1.5 h-1.5 rounded-full flex-shrink-0" :style="{ background: col.color }"></span>
                    {{ col.title }}
                    <span class="ml-auto bg-white/[0.06] rounded px-1.5 py-px text-[0.65rem]">{{ col.count }}</span>
                  </div>
                  <div v-for="task in col.tasks" :key="task.title"
                    :class="['bg-[#161c2d] border rounded-[7px] p-2.5 flex flex-col gap-2 transition-colors hover:border-indigo-500/30',
                      task.active ? 'border-amber-500/30' : task.done ? 'border-white/[0.06] opacity-50' : 'border-white/[0.06]']">
                    <div class="text-[0.72rem] text-slate-300 leading-snug">{{ task.title }}</div>
                    <div v-if="task.progress" class="flex items-center gap-1.5">
                      <div class="flex-1 h-px bg-white/[0.08] rounded overflow-hidden">
                        <div class="h-full bg-amber-400 rounded" :style="{ width: task.progress + '%' }"></div>
                      </div>
                      <span class="text-[0.6rem] text-slate-500">{{ task.progress }}%</span>
                    </div>
                    <div class="flex justify-between items-center">
                      <span :class="['text-[0.6rem] px-1.5 py-px rounded font-medium', task.tagClass]">{{ task.tag }}</span>
                      <div class="w-5 h-5 rounded-full flex items-center justify-center text-[0.55rem] font-bold text-white" :style="{ background: task.avatarColor }">{{ task.avatar }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Floating cards -->
        <div class="animate-float absolute -right-15 top-15 bg-[#161c2d] border border-white/10 rounded-xl px-4 py-3.5 flex items-center gap-3 shadow-[0_20px_60px_rgba(0,0,0,0.4)]">
          <div class="w-9 h-9 bg-indigo-500/15 rounded-lg flex items-center justify-center text-indigo-400">✓</div>
          <div>
            <div class="font-['Syne',sans-serif] text-xl font-bold text-white">8</div>
            <div class="text-[0.72rem] text-slate-500">Closed today</div>
          </div>
        </div>

        <div class="animate-float-delayed absolute -left-12 bottom-20 bg-[#161c2d] border border-white/10 rounded-xl px-4 py-3.5 flex items-center gap-3 shadow-[0_20px_60px_rgba(0,0,0,0.4)]">
          <div class="w-9 h-9 bg-indigo-500/15 rounded-lg flex items-center justify-center text-indigo-400">⚡</div>
          <div>
            <div class="font-['Syne',sans-serif] text-xl font-bold text-white">3</div>
            <div class="text-[0.72rem] text-slate-500">Overdue</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="relative z-[1] px-15 py-15 max-w-[1100px] mx-auto">
      <div class="grid grid-cols-4 gap-5">
        <div v-for="f in features" :key="f.title"
          class="bg-white/[0.02] border border-white/[0.06] rounded-2xl p-7 transition-all duration-200 hover:border-indigo-500/30 hover:-translate-y-1 cursor-default">
          <div class="text-2xl mb-4">{{ f.icon }}</div>
          <h3 class="font-['Syne',sans-serif] text-base font-bold text-white mb-2.5">{{ f.title }}</h3>
          <p class="text-sm text-slate-500 leading-relaxed">{{ f.desc }}</p>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="relative z-[1] text-center px-10 py-20 border-t border-white/[0.05]">
      <h2 class="font-['Syne',sans-serif] text-[clamp(2rem,4vw,3rem)] font-extrabold text-white mb-4">Ready to ship faster?</h2>
      <p class="text-slate-500 text-base mb-9">Join teams already using TaskFlow to stay on track.</p>
      <button class="inline-flex items-center gap-2 bg-indigo-500 text-white border-none font-['DM_Sans',sans-serif] text-base font-medium px-8 py-3.5 rounded-[10px] cursor-pointer hover:bg-indigo-600 hover:-translate-y-px transition-all">
        Create free workspace →
      </button>
    </section>

  </div>
</template>

<script setup>
import { ref } from 'vue'

const sidebarItems = ref([
  { icon: '⊞', label: 'Board', active: true },
  { icon: '≡', label: 'List', active: false },
  { icon: '◷', label: 'Timeline', active: false },
  { icon: '◉', label: 'Members', active: false },
])

const kanbanCols = ref([
  {
    title: 'To Do', color: '#6b7280', count: 4,
    tasks: [
      { title: 'Setup CI/CD pipeline', tag: 'DevOps', tagClass: 'bg-blue-400/15 text-blue-400', avatar: 'K', avatarColor: '#60a5fa' },
      { title: 'Write API documentation', tag: 'Docs', tagClass: 'bg-violet-400/15 text-violet-400', avatar: 'A', avatarColor: '#a78bfa' },
    ]
  },
  {
    title: 'In Progress', color: '#f59e0b', count: 5,
    tasks: [
      { title: 'Build user auth flow', tag: 'Backend', tagClass: 'bg-emerald-400/15 text-emerald-400', avatar: 'J', avatarColor: '#34d399', active: true, progress: 65 },
      { title: 'Design task board UI', tag: 'Design', tagClass: 'bg-red-400/15 text-red-400', avatar: 'M', avatarColor: '#f87171' },
    ]
  },
  {
    title: 'Done', color: '#10b981', count: 5,
    tasks: [
      { title: 'Init Django project', tag: 'Backend', tagClass: 'bg-blue-400/15 text-blue-400', avatar: 'K', avatarColor: '#60a5fa', done: true },
      { title: 'Setup PostgreSQL', tag: 'DevOps', tagClass: 'bg-blue-400/15 text-blue-400', avatar: 'J', avatarColor: '#34d399', done: true },
    ]
  }
])

const features = ref([
  { icon: '⊞', title: 'Kanban Board', desc: 'Drag and drop tasks across columns. Visualize your workflow at a glance.' },
  { icon: '◉', title: 'Team Management', desc: 'Assign tasks, set roles, and track who is working on what in real time.' },
  { icon: '◷', title: 'Timeline View', desc: 'See deadlines and dependencies laid out across a clear project timeline.' },
  { icon: '⚡', title: 'Fast & Reliable', desc: 'Built on Django and PostgreSQL. 12ms average response. 98% uptime.' }
])

function getStarted() {
  console.log('navigate to register')
}
</script>
