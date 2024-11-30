import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Login from '../components/Login.vue'
import MainLayout from '../components/MainLayout.vue'
import EnglishEssay from '../components/EnglishEssay.vue'
import History from '../components/History.vue'
import Profile from '../components/Profile.vue'
import AdminPanel from '../components/AdminPanel.vue'
import NotFound from '../components/NotFound.vue'
import { authStore } from '../stores/auth'
import TermsOfService from '../components/TermsOfService.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/app',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: 'english-essay',
        name: 'english-essay',
        component: EnglishEssay
      },
      {
        path: 'history',
        name: 'history',
        component: History
      },
      {
        path: 'profile',
        name: 'profile',
        component: Profile
      },
      {
        path: 'admin',
        name: 'admin',
        component: AdminPanel,
        meta: { requiresAdmin: true }
      }
    ]
  },
  {
    path: '/terms',
    name: 'terms',
    component: TermsOfService
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFound
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !authStore.isAuthenticated()) {
    next('/login')
  } else if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next('/app/english-essay')
  } else {
    next()
  }
})

export default router 