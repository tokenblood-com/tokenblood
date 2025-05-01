import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import TaskView from '@/views/TaskView.vue'
import LeaderboardView from '@/views/LeaderboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView
    },
    {
      path: '/tasks/:name',
      name: 'task',
      component: TaskView
    },
    {
      path: '/leaderboard',
      name: 'leaderboard',
      component: LeaderboardView
    }
  ]
})

export default router
