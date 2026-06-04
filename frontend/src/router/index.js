import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AuthView from '../views/AuthView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/home',
    },
    {
      path: '/login',
      name: 'login',
      component: AuthView,
    },
    {
      path: '/home',
      name: 'home',
      component: HomeView,
      meta: { activeView: 'groups' },
    },
    {
      path: '/group',
      name: 'group-list',
      component: HomeView,
      meta: { activeView: 'groups' },
    },
    {
      path: '/group/:id',
      name: 'group',
      component: HomeView,
      meta: { activeView: 'board' },
    },
    {
      path: '/my-tasks',
      name: 'my-tasks',
      component: HomeView,
      meta: { activeView: 'my-tasks' },
    },
    {
      path: '/users',
      redirect: '/home',
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
  ],
})

router.beforeEach((to) => {
  const hasToken = Boolean(localStorage.getItem('access_token'))

  if (to.name === 'login' && hasToken) {
    return { name: 'home' }
  }

  if (to.name !== 'login' && !hasToken) {
    return { name: 'login' }
  }
})

export default router
