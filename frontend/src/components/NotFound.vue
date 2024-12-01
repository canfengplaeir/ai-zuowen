<template>
  <div class="min-h-screen flex items-center justify-center bg-base-200">
    <div class="text-center space-y-6 p-4">
      <div class="text-9xl font-bold text-primary">404</div>
      <h1 class="text-4xl font-bold">页面不存在</h1>
      <p class="text-base-content/70">抱歉，您访问的页面不存在或已被移除</p>
      <div class="flex justify-center gap-4 mt-8">
        <button class="btn btn-primary" @click="goBack">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          返回上一页
        </button>
        <router-link to="/" class="btn">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          返回首页
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  // 如果有上一页历史，则返回上一页
  if (window.history.length > 1) {
    router.back()
  } else {
    // 如果没有历史记录，则返回首页
    router.push('/')
  }
}
</script>

<style scoped>
/* 添加一些动画效果 */
.text-9xl {
  @apply animate-bounce;
  animation-duration: 2s;
}

.btn {
  @apply transition-all duration-200;
}

.btn:hover {
  @apply transform -translate-y-1;
}
</style> 