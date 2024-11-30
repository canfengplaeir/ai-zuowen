<template>
  <div class="layout-container">
    <!-- 移动端顶部导航栏 -->
    <div v-if="isMobile" class="mobile-header">
      <label for="mobile-menu" class="btn btn-ghost btn-sm">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7" />
        </svg>
      </label>
      <div class="flex items-center gap-2">
        <div class="avatar placeholder">
          <div class="bg-primary text-primary-content rounded-lg w-8">
            <span class="text-lg">AI</span>
          </div>
        </div>
        <h1 class="text-lg font-bold">作文批改系统</h1>
      </div>
    </div>

    <!-- 桌面端顶部栏 -->
    <div v-if="!isMobile" class="desktop-header">
      <div class="flex items-center justify-between px-4 h-16">
        <h1 class="text-lg font-bold">作文批改系统</h1>
        <button class="btn btn-ghost btn-sm" @click="toggleSidebar">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" :class="{ 'rotate-180': !isExpanded }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
      </div>
    </div>

    <!-- 桌面端侧边栏 -->
    <div v-if="!isMobile" class="sidebar" :class="{ 'collapsed': !isExpanded }">
      <!-- 顶部区域 -->
      <div class="sidebar-header">
        <div class="logo-container">
          <div class="avatar placeholder">
            <div class="bg-primary text-primary-content rounded-lg w-10">
              <span class="text-xl">AI</span>
            </div>
          </div>
          <h1 class="logo-text" v-show="isExpanded">作文批改系统</h1>
        </div>
        <button class="collapse-btn" @click="toggleSidebar">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" :class="{ 'rotate-180': !isExpanded }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
      </div>

      <!-- 菜单区域 -->
      <div class="sidebar-menu">
        <!-- 作文批改 -->
        <div class="menu-section">
          <div class="menu-title" v-show="isExpanded">作文批改</div>
          <ul class="menu-list">
            <li>
              <router-link 
                to="/app/english-essay" 
                class="menu-item"
                :class="{ 'menu-item-active': $route.path === '/app/english-essay' }"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="menu-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                <span v-show="isExpanded">英语作文批改</span>
              </router-link>
            </li>
            <li>
              <a class="disabled">
                <svg xmlns="http://www.w3.org/2000/svg" class="menu-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span v-if="isExpanded">
                  语文作文批改
                  <span class="badge badge-sm">开发中</span>
                </span>
              </a>
            </li>
          </ul>
        </div>

        <!-- 历史记录 -->
        <div class="menu-section">
          <div class="menu-title" v-show="isExpanded">历史记录</div>
          <ul class="menu-list">
            <li>
              <router-link 
                to="/app/history" 
                class="menu-item"
                :class="{ 'menu-item-active': $route.path === '/app/history' }"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="menu-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span v-show="isExpanded">批改历史</span>
              </router-link>
            </li>
          </ul>
        </div>

        <!-- 个人中心 -->
        <div class="menu-section">
          <div class="menu-title" v-show="isExpanded">个人中心</div>
          <ul class="menu-list">
            <li>
              <router-link 
                to="/app/profile" 
                class="menu-item"
                :class="{ 'menu-item-active': $route.path === '/app/profile' }"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="menu-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                <span v-show="isExpanded">个人信息</span>
              </router-link>
            </li>
            <li v-if="authStore.isAdmin">
              <router-link 
                to="/app/admin" 
                class="menu-item"
                :class="{ 'menu-item-active': $route.path === '/app/admin' }"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="menu-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span v-show="isExpanded">管理员面板</span>
              </router-link>
            </li>
          </ul>
        </div>
      </div>

      <!-- 底部退出按钮 -->
      <div class="sidebar-footer">
        <a @click="handleLogout" class="logout-btn">
          <svg xmlns="http://www.w3.org/2000/svg" class="menu-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          <span v-show="isExpanded">退出登录</span>
        </a>
      </div>
    </div>

    <!-- 移动端抽屉菜单 -->
    <div class="drawer drawer-end">
      <input id="mobile-menu" type="checkbox" class="drawer-toggle" v-model="isMobileMenuOpen" />
      <div class="drawer-side">
        <label for="mobile-menu" class="drawer-overlay"></label>
        <div class="menu p-4 w-80 min-h-full bg-base-200">
          <!-- 移动端菜单内容 -->
          <div class="flex items-center gap-3 mb-6">
            <div class="avatar placeholder">
              <div class="bg-primary text-primary-content rounded-lg w-10">
                <span class="text-xl">AI</span>
              </div>
            </div>
            <h1 class="text-xl font-bold">作文批改系统</h1>
          </div>

          <!-- 作文批改 -->
          <div class="menu-section">
            <div class="menu-title">作文批改</div>
            <ul class="menu-list">
              <li>
                <router-link 
                  to="/app/english-essay" 
                  class="menu-item"
                  :class="{ 'menu-item-active': $route.path === '/app/english-essay' }"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="menu-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                  <span>英语作文批改</span>
                </router-link>
              </li>
              <li>
                <a class="disabled">
                  <svg xmlns="http://www.w3.org/2000/svg" class="menu-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <span>语文作文批改</span>
                  <span class="badge badge-sm">开发中</span>
                </a>
              </li>
            </ul>
          </div>

          <!-- 历史记录 -->
          <div class="menu-section">
            <div class="menu-title">历史记录</div>
            <ul class="menu-list">
              <li>
                <router-link 
                  to="/app/history" 
                  class="menu-item"
                  :class="{ 'menu-item-active': $route.path === '/app/history' }"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="menu-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>批改历史</span>
                </router-link>
              </li>
            </ul>
          </div>

          <!-- 个人中心 -->
          <div class="menu-section">
            <div class="menu-title">个人中心</div>
            <ul class="menu-list">
              <li>
                <router-link 
                  to="/app/profile" 
                  class="menu-item"
                  :class="{ 'menu-item-active': $route.path === '/app/profile' }"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="menu-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  <span>个人信息</span>
                </router-link>
              </li>
              <li v-if="authStore.isAdmin">
                <router-link 
                  to="/app/admin" 
                  class="menu-item"
                  :class="{ 'menu-item-active': $route.path === '/app/admin' }"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="menu-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <span>管理员面板</span>
                </router-link>
              </li>
            </ul>
          </div>

          <!-- 退出登录 -->
          <div class="mt-auto">
            <a @click="handleLogout" class="logout-btn">
              <svg xmlns="http://www.w3.org/2000/svg" class="menu-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              <span>退出登录</span>
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="main-content" :class="{ 
      'content-expanded': !isExpanded && !isMobile,
      'md:ml-[280px]': !isExpanded && !isMobile,
      'md:ml-20': isExpanded && !isMobile,
      'pt-16': isMobile
    }">
      <slot></slot>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { useConfirm } from './ConfirmDialog.vue'
import { authStore } from '../stores/auth'

export default {
  name: 'Sidebar',
  props: {
    currentView: String
  },
  emits: ['change-view', 'logout'],
  
  setup(props, { emit }) {
    const isExpanded = ref(true)
    const isMobileMenuOpen = ref(false)
    const isMobile = ref(false)
    const confirm = useConfirm()

    // 检查是否为移动设备
    const checkMobile = () => {
      isMobile.value = window.innerWidth < 768
    }

    // 监听窗口大小变化
    onMounted(() => {
      checkMobile()
      window.addEventListener('resize', checkMobile)
    })

    onUnmounted(() => {
      window.removeEventListener('resize', checkMobile)
    })

    const toggleSidebar = () => {
      isExpanded.value = !isExpanded.value
    }

    const toggleMobileMenu = () => {
      isMobileMenuOpen.value = !isMobileMenuOpen.value
    }

    const handleLogout = async () => {
      const confirmed = await confirm.showConfirm(
        '退出登录',
        '确定要退出登录吗？'
      )
      if (confirmed) {
        isMobileMenuOpen.value = false
        emit('logout')
      }
    }

    const handleMenuClick = (view) => {
      isMobileMenuOpen.value = false
      emit('change-view', view)
    }

    return { 
      isExpanded,
      isMobileMenuOpen,
      isMobile,
      toggleSidebar,
      toggleMobileMenu,
      handleLogout,
      authStore,
      handleMenuClick
    }
  }
}
</script>

<style scoped>
.layout-container {
  @apply flex min-h-screen flex-col md:flex-row;
}

.mobile-header {
  @apply fixed top-0 left-0 right-0 h-16 px-4 flex items-center  bg-base-100 border-b border-base-300 z-40;
}

.desktop-header {
  @apply fixed top-0 left-0 right-0 bg-base-100 border-b border-base-300 z-30;
  margin-right: 280px;
  transition: margin-right 0.3s ease;
}

.desktop-header button {
  transition: transform 0.3s ease;
}

.collapsed ~ .desktop-header {
  margin-right: 80px;
}

.sidebar {
  @apply fixed top-0 left-0 h-full bg-base-200 flex flex-col transition-all duration-300 ease-in-out z-20;
  width: 280px;
  transform: translateX(0);
}

.sidebar.collapsed {
  width: 80px;
  transform: translateX(0);
}

.sidebar-header {
  @apply p-4 flex items-center justify-between border-b border-base-300;
}

.logo-container {
  @apply flex items-center gap-3;
}

.logo-text {
  @apply text-xl font-bold transition-opacity duration-300;
}

.collapse-btn {
  @apply btn btn-ghost btn-sm p-1;
  position: absolute;
  right: -12px;
  top: 50%;
  transform: translateY(-50%);
  background: var(--b2);
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 30;
}

.sidebar-menu {
  @apply flex-1 overflow-y-auto py-4;
}

.menu-section {
  @apply mb-6;
}

.menu-title {
  @apply px-4 text-xs font-semibold uppercase text-base-content/50 mb-2;
}

.menu-list {
  @apply space-y-1;
}

.menu-list li a {
  @apply flex items-center gap-3 px-4 py-2 text-base-content/70 hover:bg-base-300 transition-colors duration-200 cursor-pointer;
}

.menu-list li a.active {
  @apply bg-primary text-primary-content;
}

.menu-list li a.disabled {
  @apply opacity-50 cursor-not-allowed;
}

.menu-icon {
  @apply h-5 w-5 flex-shrink-0;
}

.sidebar-footer {
  @apply p-4 border-t border-base-300;
}

.logout-btn {
  @apply flex items-center gap-3 px-4 py-2 text-error hover:bg-error hover:text-error-content rounded-lg transition-colors duration-200 cursor-pointer;
}

.main-content {
  @apply flex-1 transition-all duration-300 ease-in-out;
  min-height: calc(100vh - 4rem);
}

@media (min-width: 768px) {
  .main-content {
    margin-left: 280px;
  }
  
  .content-expanded {
    margin-left: 80px;
  }
}

/* 动画过渡 */
.rotate-180 {
  transform: rotate(180deg);
}

/* 滚动条样式 */
.sidebar-menu::-webkit-scrollbar {
  width: 4px;
}

.sidebar-menu::-webkit-scrollbar-track {
  @apply bg-transparent;
}

.sidebar-menu::-webkit-scrollbar-thumb {
  @apply bg-base-300 rounded;
}

/* 移动端样式 */
.drawer {
  @apply z-30;
}

.drawer-side {
  @apply fixed top-0 right-0 w-80 h-full z-50;
}

.drawer-overlay {
  @apply fixed inset-0 bg-black bg-opacity-50;
}

/* 确保移动端菜单在桌面端不可见 */
@media (min-width: 768px) {
  .drawer {
    display: none;
  }
}

.menu-item {
  @apply flex items-center gap-3 px-4 py-3 rounded-lg text-base-content/70 hover:bg-base-300 transition-all duration-200;
}

.menu-item-active {
  @apply bg-primary text-primary-content hover:bg-primary/90;
  position: relative;
}

.menu-item-active::before {
  content: '';
  @apply absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-primary-content rounded-r;
}

.menu-item-active .menu-icon {
  @apply text-primary-content;
}

.menu-item:hover {
  @apply transform scale-[1.02];
}

/* 动画效果 */
.menu-item {
  transition: all 0.2s ease;
}

.menu-item-active {
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