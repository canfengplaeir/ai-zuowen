import { createRouter, createWebHistory } from 'vue-router'
import { authStore } from '../stores/auth'
import EnglishEssay from '../components/EnglishEssay.vue'
import History from '../components/History.vue'
import Profile from '../components/Profile.vue'
import AdminPanel from '../components/AdminPanel.vue'
import Login from '../components/Login.vue'
import Home from '../components/Home.vue'
import MainLayout from '../layouts/MainLayout.vue'
import NotFound from '../components/NotFound.vue'

const routes = [
  {
    path: '/',
    component: Home,
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/app',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/app/english-essay'
      },
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
  // 404 路由必须放在最后
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
  const isAuthenticated = authStore.isAuthenticated()
  
  // 不需要认证的路由直接通过
  if (!to.meta.requiresAuth) {
    if (isAuthenticated && to.name === 'login') {
      next('/app/english-essay')
    } else {
      next()
    }
    return
  }
  
  // 需要认证但未登录
  if (!isAuthenticated) {
    next('/login')
    return
  }
  
  // 需要管理员权限但不是管理员
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next('/app/english-essay')
    return
  }
  
  next()
})

export default router 