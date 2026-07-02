import { createRouter, createWebHistory } from 'vue-router'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/pages/LoginPage.vue'),
      meta: { guestOnly: true },
    },
    {
      path: '/admin',
      name: 'AdminPrerequisites',
      component: () => import('@/pages/AdminPrerequisitesPage.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
      path: '/admin/questions',
      name: 'AdminQuestions',
      component: () => import('@/pages/AdminQuestionsPage.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
      path: '/admin/materials',
      name: 'AdminMaterials',
      component: () => import('@/pages/AdminMaterialsPage.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
      path: '/gamification',
      name: 'Gamification',
      component: () => import('@/pages/GamificationPage.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('@/pages/ProfilePage.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/',
      component: DashboardLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'Dashboard',
          component: () => import('@/pages/DashboardPage.vue'),
        },
      ],
    },
  ],
})

router.beforeEach(async (to) => {
  const userStore = useUserStore()

  if (userStore.token && !userStore.currentUser) {
    await userStore.initAuth()
  }

  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    return { name: 'Login' }
  }

  if (to.meta.requiresAdmin && userStore.currentUser?.role !== 'admin') {
    return { name: 'Dashboard' }
  }

  if (to.meta.guestOnly && userStore.isAuthenticated) {
    return { name: 'Dashboard' }
  }

  return true
})

export default router
