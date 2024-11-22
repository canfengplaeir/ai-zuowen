<template>
  <div>
    <!-- 导航栏 -->
    <nav class="navbar bg-base-100 fixed top-0 z-50 shadow-lg">
      <div class="container mx-auto px-4">
        <div class="flex-1">
          <a class="text-xl font-bold flex items-center gap-2">
            <div class="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
              <span class="text-primary-content text-xl">AI</span>
            </div>
            AI作文批改系统
          </a>
        </div>
        <div class="flex-none gap-4">
          <router-link 
            v-if="!authStore.isAuthenticated()" 
            to="/login" 
            class="btn btn-primary"
          >
            登录 / 注册
          </router-link>
          <router-link 
            v-else 
            to="/app/english-essay" 
            class="btn btn-primary"
          >
            进入系统
          </router-link>
        </div>
      </div>
    </nav>

    <!-- 英雄区域 -->
    <div class="hero min-h-screen bg-base-200 pt-16">
      <div class="hero-content text-center">
        <div class="max-w-3xl">
          <h1 class="text-5xl font-bold mb-8 bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
            智能批改，助力提升
          </h1>
          <p class="text-xl mb-8 text-base-content/80 text-white">
            使用先进的人工智能技术，为您提供专业、快速、准确的作文批改服务
          </p>
          <router-link 
            :to="authStore.isAuthenticated() ? '/app/english-essay' : '/login'"
            class="btn btn-primary btn-lg"
          >
            {{ authStore.isAuthenticated() ? '开始批改' : '立即体验' }}
          </router-link>
        </div>
      </div>
    </div>

    <!-- 功能特点 -->
    <div class="py-24 bg-base-100">
      <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold text-center mb-16">系统特点</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- AI智能批改 -->
          <div class="card bg-base-200 shadow-xl hover:shadow-2xl transition-shadow">
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

    <!-- 使用步骤 -->
    <div class="py-24 bg-base-200">
      <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold text-center mb-16">使用步骤</h2>
        <ul class="steps steps-vertical lg:steps-horizontal w-full">
          <li class="step step-primary">选择作文图片</li>
          <li class="step step-primary">调整图片内容</li>
          <li class="step step-primary">获取批改结果</li>
          <li class="step step-primary">查看详细分析</li>
        </ul>
      </div>
    </div>

    <!-- 开始使用 CTA -->
    <div class="py-24 bg-base-100 text-center">
      <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold mb-8">准备好提升写作水平了吗？</h2>
        <p class="text-xl mb-8 text-base-content/70">立即开始使用我们的AI作文批改系统</p>
        <router-link 
          :to="authStore.isAuthenticated() ? '/app/english-essay' : '/login'"
          class="btn btn-primary btn-lg"
        >
          {{ authStore.isAuthenticated() ? '开始批改' : '立即注册' }}
        </router-link>
      </div>
    </div>

    <!-- 页脚 -->
    <footer class="footer footer-center p-10 bg-base-200 text-base-content">
      <div>
        <p class="font-bold">
          AI作文批改系统
        </p>
        <p>智能批改 · 专业分析 · 持续提升</p>
        <p>Copyright © 2024 - All rights reserved</p>
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

.steps-horizontal .step:before,
.steps-horizontal .step:after {
  @apply bg-base-300;
}

.step-primary:before,
.step-primary:after {
  @apply bg-primary;
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

.bg-gradient-to-r {
  background-size: 200% auto;
  animation: gradient 3s ease infinite;
}
</style> 