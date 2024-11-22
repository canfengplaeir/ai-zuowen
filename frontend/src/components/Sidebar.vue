<template>
  <div class="layout-container">
    <!-- 侧边栏 -->
    <div class="sidebar" :class="{ 'collapsed': !isExpanded }">
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
              <a @click="$emit('change-view', 'english-essay')" 
                 :class="{ 'active': currentView === 'english-essay' }">
                <svg xmlns="http://www.w3.org/2000/svg" class="menu-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                <span v-show="isExpanded">英语作文批改</span>
              </a>
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
              <a @click="$emit('change-view', 'history')" 
                 :class="{ 'active': currentView === 'history' }">
                <svg xmlns="http://www.w3.org/2000/svg" class="menu-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span v-show="isExpanded">批改历史</span>
              </a>
            </li>
          </ul>
        </div>

        <!-- 个人中心 -->
        <div class="menu-section">
          <div class="menu-title" v-show="isExpanded">个人中心</div>
          <ul class="menu-list">
            <li>
              <a @click="$emit('change-view', 'profile')" 
                 :class="{ 'active': currentView === 'profile' }">
                <svg xmlns="http://www.w3.org/2000/svg" class="menu-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                <span v-show="isExpanded">个人信息</span>
              </a>
            </li>
            <li v-if="isAdmin">
              <a @click="$emit('change-view', 'admin')" 
                 :class="{ 'active': currentView === 'admin' }">
                <svg xmlns="http://www.w3.org/2000/svg" class="menu-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span v-show="isExpanded">管理员面板</span>
              </a>
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

    <!-- 主内容区域 -->
    <div class="main-content" :class="{ 'content-expanded': !isExpanded }">
      <slot></slot>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useConfirm } from './ConfirmDialog.vue'

export default {
  name: 'Sidebar',
  props: {
    currentView: {
      type: String,
      required: true
    },
    isAdmin: {
      type: Boolean,
      default: false
    }
  },
  setup(props, { emit }) {
    const isExpanded = ref(true)
    const confirm = useConfirm()

    const toggleSidebar = () => {
      isExpanded.value = !isExpanded.value
    }

    const handleLogout = async () => {
      const confirmed = await confirm.showConfirm(
        '退出登录',
        '确定要退出登录吗？'
      )
      if (confirmed) {
        emit('logout')
      }
    }

    return { 
      isExpanded,
      toggleSidebar,
      handleLogout
    }
  }
}
</script>

<style scoped>
.layout-container {
  @apply flex min-h-screen;
}

.sidebar {
  @apply fixed top-0 left-0 h-full bg-base-200 flex flex-col transition-all duration-300 ease-in-out z-20;
  width: 280px;
}

.sidebar.collapsed {
  width: 80px;
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
  @apply ml-[280px] flex-1 transition-all duration-300 ease-in-out;
}

.main-content.content-expanded {
  @apply ml-20;
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
</style>