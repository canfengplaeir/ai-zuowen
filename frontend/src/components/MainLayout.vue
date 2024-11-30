<template>
  <div class="drawer lg:drawer-open">
    <!-- 抽屉控制器 -->
    <input id="main-drawer" type="checkbox" class="drawer-toggle" v-model="isDrawerOpen" />
    
    <!-- 主内容区域 -->
    <div class="drawer-content flex flex-col min-h-screen">
      <!-- 顶部导航栏 -->
      <div class="navbar bg-base-100 lg:hidden">
        <div class="flex-none">
          <label for="main-drawer" class="btn btn-square btn-ghost drawer-button">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="inline-block w-5 h-5 stroke-current">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
            </svg>
          </label>
        </div>
        <div class="flex-1">
          <h1 class="text-xl font-bold">AI作文批改系统</h1>
        </div>
      </div>

      <!-- 页面内容 -->
      <main class="flex-1 p-4 lg:p-6">
        <div class="max-w-[1200px] mx-auto">
          <Transition
            enter-active-class="transition-opacity duration-200 ease-out"
            enter-from-class="opacity-0"
            enter-to-class="opacity-100"
            leave-active-class="transition-opacity duration-150 ease-in"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
          >
            <!-- 加载动画 -->
            <div v-if="loading" class="fixed inset-0 bg-base-100 bg-opacity-50 backdrop-blur-sm z-50">
              <div class="flex flex-col items-center justify-center min-h-screen">
                <div class="loading loading-spinner loading-lg text-primary"></div>
                <p class="mt-4 text-base-content/70">{{ loadingText || '加载中...' }}</p>
              </div>
            </div>
          </Transition>
          
          <!-- 路由内容 -->
          <router-view v-slot="{ Component }">
            <transition 
              name="fade"
              mode="out-in"
            >
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </main>
    </div>

    <!-- 侧边栏内容 -->
    <div class="drawer-side z-40">
      <label for="main-drawer" class="drawer-overlay"></label>
      <div class="menu p-4 w-72 min-h-full bg-base-200 flex flex-col">
        <!-- Logo -->
        <div class="flex items-center gap-3 mb-6 px-2">
          <div class="avatar placeholder">
            <div class="bg-primary text-primary-content rounded-lg w-10">
              <span class="text-base">AI</span>
            </div>
          </div>
          <h1 class="text-xl font-semibold">作文批改系统</h1>
        </div>

        <!-- 分割线 -->
        <div class="divider my-2"></div>

        <!-- 作文批改菜单组 -->
        <div class="menu-group">
          <div class="menu-title">作文批改</div>
          <ul class="menu menu-md gap-1">
            <li>
              <router-link to="/app/english-essay" class="menu-item">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                <span>英语作文批改</span>
              </router-link>
            </li>
          </ul>
        </div>

        <!-- 分割线 -->
        <div class="divider my-2"></div>

        <!-- 历史记录菜单组 -->
        <div class="menu-group">
          <div class="menu-title">历史记录</div>
          <ul class="menu menu-md gap-1">
            <li>
              <router-link to="/app/history" class="menu-item">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>批改历史</span>
              </router-link>
            </li>
          </ul>
        </div>

        <!-- 分割线 -->
        <div class="divider my-2"></div>

        <!-- 个人中心菜单组 -->
        <div class="menu-group">
          <div class="menu-title">个人中心</div>
          <ul class="menu menu-md gap-1">
            <li>
              <router-link to="/app/profile" class="menu-item">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                <span>个人信息</span>
              </router-link>
            </li>
            
            <!-- 管理员面板 -->
            <li v-if="authStore.isAdmin">
              <router-link to="/app/admin" class="menu-item">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span>管理员面板</span>
              </router-link>
            </li>
          </ul>
        </div>

        <!-- 占位符，确保退出按钮在底部 -->
        <div class="flex-1"></div>

        <!-- 退出登录按钮 -->
        <div class="mt-2">
          <div class="divider my-2"></div>
          <button 
            @click="handleLogout" 
            class="btn btn-block btn-error btn-outline gap-2 hover:scale-[1.02] transition-transform"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            退出登录
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watchEffect, provide } from 'vue'
import { useBreakpoints } from '@vueuse/core'
import { useRouter } from 'vue-router'
import { authStore } from '../stores/auth'
import { useConfirm } from './ConfirmDialog.vue'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

// 配置 NProgress
NProgress.configure({ 
  showSpinner: false,
  minimum: 0.1,
  speed: 200,
  easing: 'ease',
  trickleSpeed: 200
})

const router = useRouter()
const confirm = useConfirm()
const isDrawerOpen = ref(false)

const breakpoints = useBreakpoints({
  mobile: 640,
  tablet: 768,
  desktop: 1024,
})

// 监听断点变化
watchEffect(() => {
  if (breakpoints.greater('desktop')) {
    isDrawerOpen.value = true
  }
})

// 退出登录
const handleLogout = async () => {
  const confirmed = await confirm.showConfirm(
    '退出登录',
    '确定要退出登录吗？'
  )
  if (confirmed) {
    authStore.clearAuth()
    router.push('/login')
  }
}

// 加载状态管理
const loading = ref(false)
const loadingText = ref('')

// 提供加载状态给子组件
provide('setLoading', (value, text = '') => {
  loading.value = value
  loadingText.value = text
  if (value) {
    NProgress.start()
  } else {
    NProgress.done()
  }
})

// 路由过渡动画处理
const onTransitionStart = () => {
  loading.value = true
  NProgress.start()
}

const onTransitionEnd = () => {
  loading.value = false
  NProgress.done()
}

// 监听路由变化
router.beforeEach(() => { NProgress.start() })
router.afterEach(() => { NProgress.done() })
</script>

<style scoped>
/* 自定义样式 */
.drawer-content {
  @apply transition-all duration-300;
}

.drawer-side {
  @apply transition-transform duration-300;
}

/* 桌面端样式 */
@media (min-width: 1024px) {
  .drawer-content {
    width: 100%;
    max-width: none;
  }
  
  .drawer-side {
    transform: translateX(0) !important;
  }

  /* 主内容区域样式 */
  main {
    width: 100%;
    padding: 1.5rem;
  }
}

/* 移动端样式 */
@media (max-width: 1023px) {
  .drawer-content {
    width: 100%;
  }

  main {
    padding: 1rem;
  }
}

/* 加载遮罩层动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 加载动画容器 */
.loading-container {
  @apply fixed inset-0 flex items-center justify-center bg-base-100/50 backdrop-blur-sm z-50;
}

.loading-spinner {
  @apply w-16 h-16 text-primary;
}

/* 自定义 NProgress 样式 */
#nprogress .bar {
  background: var(--p); /* 使用主题的 primary 颜色 */
  height: 3px;
}

#nprogress .peg {
  box-shadow: 0 0 10px var(--p), 0 0 5px var(--p);
}

.menu-group {
  @apply space-y-2;
}

.menu-title {
  @apply text-xs font-semibold text-base-content/50 uppercase px-4;
}

.menu-item {
  @apply flex items-center gap-3 px-4 py-2 rounded-lg text-base-content/70 hover:bg-base-300 transition-all duration-200;
}

.menu-item.router-link-active {
  @apply bg-primary text-primary-content hover:bg-primary/90;
}

.menu-item.router-link-active::before {
  content: '';
  @apply absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-primary-content rounded-r;
}

.divider {
  @apply opacity-20;
}

/* 动画效果 */
.menu-item {
  transition: all 0.2s ease;
}

.menu-item:hover {
  @apply transform scale-[1.02];
}

.menu-item.router-link-active {
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    transform: translateX(-10px);
    opacity: 0.5;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
</style> 