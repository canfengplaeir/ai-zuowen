<template>
  <div>
    <!-- 导航栏 -->
    <nav class="navbar bg-base-100 fixed top-0 z-50 shadow-lg">
      <div class="container mx-auto px-4">
        <div class="flex-1">
          <a class="text-xl font-bold flex items-center gap-2">
            <div class="w-8 md:w-10 h-8 md:h-10 bg-primary rounded-lg flex items-center justify-center">
              <span class="text-primary-content text-lg md:text-xl">AI</span>
            </div>
            <span class="hidden sm:inline">AI作文批改系统</span>
          </a>
        </div>
        <div class="flex-none gap-2">
          <router-link 
            v-if="!authStore.isAuthenticated()" 
            to="/login" 
            class="btn btn-primary btn-sm md:btn-md"
          >
            登录 / 注册
          </router-link>
          <router-link 
            v-else 
            to="/app/english-essay" 
            class="btn btn-primary btn-sm md:btn-md"
          >
            进入系统
          </router-link>
        </div>
      </div>
    </nav>

    <!-- 英雄区域 -->
    <div class="hero min-h-screen bg-base-200 pt-16">
      <div class="hero-content text-center px-4">
        <div class="max-w-3xl">
          <h1 class="text-3xl md:text-5xl font-bold mb-4 md:mb-8 bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent animate-gradient">
            智能批改，助力提升
          </h1>
          <p class="text-base md:text-xl mb-6 md:mb-8 text-base-content/80">
            使用先进的人工智能技术，为您提供专业、快速、准确的作文批改服务
          </p>
          <router-link 
            :to="authStore.isAuthenticated() ? '/app/english-essay' : '/login'"
            class="btn btn-primary btn-wide"
          >
            {{ authStore.isAuthenticated() ? '开始批改' : '立即体验' }}
          </router-link>
        </div>
      </div>
    </div>

    <!-- 功能特点 -->
    <div class="py-12 md:py-24 bg-base-100">
      <div class="container mx-auto px-4">
        <h2 class="text-2xl md:text-3xl font-bold text-center mb-8 md:mb-16">系统特点</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8">
          <!-- AI智能批改 -->
          <div class="card bg-base-200 shadow-xl hover:shadow-2xl transition-all duration-300">
            <div class="card-body items-center text-center">
              <div class="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 class="card-title mb-2">AI智能批改</h3>
              <p class="text-base-content/70">采用先进的AI技术，提供专业的语言评估和改进建议</p>
            </div>
          </div>

          <!-- 便捷上传 -->
          <div class="card bg-base-200 shadow-xl hover:shadow-2xl transition-shadow">
            <div class="card-body items-center text-center">
              <div class="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                </svg>
              </div>
              <h3 class="card-title mb-2">便捷上传</h3>
              <p class="text-base-content/70">支持本地上传和实时拍照，轻松提交作文内容</p>
            </div>
          </div>

          <!-- 详细分析 -->
          <div class="card bg-base-200 shadow-xl hover:shadow-2xl transition-shadow">
            <div class="card-body items-center text-center">
              <div class="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 class="card-title mb-2">详细分析</h3>
              <p class="text-base-content/70">提供全面的评分和建议，帮助提升写作水平</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 开始使用 CTA -->
    <div class="py-12 md:py-24 bg-base-100 text-center">
      <div class="container mx-auto px-4">
        <h2 class="text-2xl md:text-3xl font-bold mb-4 md:mb-8">准备好提升写作水平了吗？</h2>
        <p class="text-lg md:text-xl mb-6 md:mb-8 text-base-content/70">立即开始使用我们的AI作文批改系统</p>
        <router-link 
          :to="authStore.isAuthenticated() ? '/app/english-essay' : '/login'"
          class="btn btn-primary btn-wide"
        >
          {{ authStore.isAuthenticated() ? '开始批改' : '立即注册' }}
        </router-link>
      </div>
    </div>

    <!-- 页脚 -->
    <footer class="footer footer-center p-8 md:p-10 bg-base-200 text-base-content">
      <div>
        <p class="font-bold text-lg md:text-xl">AI作文批改系统</p>
        <p class="text-base md:text-lg">智能批改 · 专业分析 · 持续提升</p>
        <p class="text-sm md:text-base">Copyright © {{ new Date().getFullYear() }} - All rights reserved</p>
      </div>
    </footer>
  </div>
</template>

<script>
import { authStore } from '../stores/auth'

export default {
  name: 'Home',
  setup() {
    return {
      authStore
    }
  }
}
</script>

<style scoped>
.hero {
  background-image: 
    linear-gradient(to bottom, rgba(0,0,0,0.3), rgba(0,0,0,0.1)),
    url('/images/hero-bg.jpg');
  background-size: cover;
  background-position: center;
}

.card {
  @apply transition-all duration-300;
}

.card:hover {
  @apply transform -translate-y-1;
}

/* 渐变文字动画 */
@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.animate-gradient {
  background-size: 200% auto;
  animation: gradient 3s ease infinite;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .hero-content {
    @apply py-8;
  }
  
  .card-body {
    @apply p-6;
  }
}
</style> 