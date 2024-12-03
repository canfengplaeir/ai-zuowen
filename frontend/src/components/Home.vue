<template>
  <div>
    <!-- 导航栏 -->
    <nav class="navbar fixed top-0 z-50">
      <!-- 亚克力效果容器 -->
      <div class="acrylic absolute inset-0"></div>
      
      <div class="container mx-auto px-4 relative z-10">
        <div class="flex-1">
          <a class="text-xl font-bold flex items-center gap-2">
            <div class="w-8 md:w-10 h-8 md:h-10 bg-primary rounded-lg flex items-center justify-center shadow-lg">
              <span class="text-primary-content text-lg md:text-xl">AI</span>
            </div>
            <span class="hidden sm:inline bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
              AI作文批改系统
            </span>
          </a>
        </div>
        <div class="flex-none gap-2">
          <router-link 
            v-if="!authStore.isAuthenticated()" 
            to="/login" 
            class="btn btn-primary btn-sm md:btn-md shadow-lg hover:shadow-xl"
          >
            登录 / 注册
          </router-link>
          <router-link 
            v-else 
            to="/app/english-essay" 
            class="btn btn-primary btn-sm md:btn-md shadow-lg hover:shadow-xl"
          >
            进入系统
          </router-link>
        </div>
      </div>
    </nav>

    <!-- 英雄区域 -->
    <div class="hero min-h-screen bg-hero relative">
      <!-- 背景遮罩 -->
      <div class="absolute inset-0 bg-gradient-to-b from-black/30 to-black/60"></div>
      
      <div class="hero-content text-center px-4 relative z-10">
        <div class="max-w-3xl space-y-8">
          <h1 class="text-3xl md:text-5xl font-bold mb-4 md:mb-8 text-white animate-title">
            智能批改，助力提升
          </h1>
          <p class="text-base md:text-xl mb-6 md:mb-8 text-white/90 animate-subtitle">
            使用先进的人工智能技术，为您提供专业、快速、准确的作文批改服务
          </p>
          <router-link 
            :to="authStore.isAuthenticated() ? '/app/english-essay' : '/login'"
            class="btn btn-primary btn-wide shadow-lg hover:shadow-xl bg-gradient-to-r from-primary to-secondary border-0 text-white animate-button"
          >
            {{ authStore.isAuthenticated() ? '开始批改' : '立即体验' }}
          </router-link>
        </div>
      </div>
    </div>

    <!-- 功能特点 -->
    <div class="py-24 bg-base-100 relative overflow-hidden">
      <!-- 装饰背景 -->
      <div class="absolute inset-0 bg-grid-pattern opacity-5"></div>
      
      <div class="container mx-auto px-4 relative z-10">
        <h2 class="text-2xl md:text-3xl font-bold text-center mb-16 animate-fade-in">系统特点</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- AI智能批改 -->
          <div class="feature-card">
            <div class="feature-icon bg-primary/10">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 class="card-title mb-2">AI智能批改</h3>
            <p class="text-base-content/70">采用先进的AI技术，提供专业的语言评估和改进建议</p>
          </div>

          <!-- 便捷上传 -->
          <div class="feature-card">
            <div class="feature-icon bg-secondary/10">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-secondary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
              </svg>
            </div>
            <h3 class="card-title mb-2">便捷上传</h3>
            <p class="text-base-content/70">支持本地上传和实时拍照，轻松提交作文内容</p>
          </div>

          <!-- 详细分析 -->
          <div class="feature-card">
            <div class="feature-icon bg-accent/10">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 class="card-title mb-2">详细分析</h3>
            <p class="text-base-content/70">提供全面的评分和建议，帮助提升写作水平</p>
          </div>
        </div>
      </div>
    </div>

    <!-- CTA 区域 -->
    <div class="py-24 bg-base-200 relative">
      <!-- 亚克力效果容器 -->
      <div class="acrylic absolute inset-0"></div>
      
      <div class="container mx-auto px-4 relative z-10 text-center">
        <h2 class="text-2xl md:text-3xl font-bold mb-8 animate-fade-in">准备好提升写作水平了吗？</h2>
        <p class="text-lg md:text-xl mb-8 text-base-content/70 animate-fade-in delay-200">
          立即开始使用我们的AI作文批改系统
        </p>
        <router-link 
          :to="authStore.isAuthenticated() ? '/app/english-essay' : '/login'"
          class="btn btn-primary btn-wide shadow-lg hover:shadow-xl bg-gradient-to-r from-primary to-secondary border-0 text-white animate-fade-in delay-400"
        >
          {{ authStore.isAuthenticated() ? '开始批改' : '立即注册' }}
        </router-link>
      </div>
    </div>

    <!-- 页脚 -->
    <footer class="footer footer-center p-8 md:p-10 bg-base-300 text-base-content relative">
      <!-- 亚克力效果容器 -->
      <div class="acrylic absolute inset-0"></div>
      
      <div class="relative z-10">
        <p class="font-bold text-lg md:text-xl">AI作文批改系统</p>
        <p class="text-base md:text-lg">智能批改 · 专业分析 · 持续提升</p>
        <p class="text-sm md:text-base opacity-60">
          Copyright © {{ new Date().getFullYear() }} - All rights reserved
        </p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
/* 亚克力效果 */
.acrylic {
  backdrop-filter: 
    blur(16px)
    brightness(110%)
    saturate(120%);
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.1) 0%,
    rgba(255, 255, 255, 0.05) 100%
  );
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* 英雄区背景 */
.bg-hero {
  background-image: url('https://objectstorageapi.bja.sealos.run/g6rnmc1y-mymy/hero-bg.jpg');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
}

/* 网格背景 */
.bg-grid-pattern {
  background-image: 
    linear-gradient(var(--p) 1px, transparent 1px),
    linear-gradient(90deg, var(--p) 1px, transparent 1px);
  background-size: 20px 20px;
}

/* 特性卡片 */
.feature-card {
  @apply card bg-base-100 shadow-xl hover:shadow-2xl transition-all duration-300 p-6 text-center animate-fade-in;
}

.feature-card:hover {
  @apply transform -translate-y-2;
}

.feature-icon {
  @apply w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 transition-all duration-300;
}

.feature-card:hover .feature-icon {
  @apply transform scale-110;
}

/* 动画效果 */
.animate-title {
  animation: slideDown 1s ease-out;
}

.animate-subtitle {
  animation: slideDown 1s ease-out 0.3s backwards;
}

.animate-button {
  animation: slideUp 1s ease-out 0.6s backwards;
}

.animate-fade-in {
  animation: fadeIn 1s ease-out;
}

.delay-200 {
  animation-delay: 0.2s;
}

.delay-400 {
  animation-delay: 0.4s;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .hero-content {
    @apply py-20;
  }
  
  .feature-card {
    @apply p-4;
  }
  
  .feature-icon {
    @apply w-12 h-12;
  }
}

/* 按钮样式增强 */
.btn {
  @apply font-medium;
}

.btn-primary {
  @apply text-white;
}

/* 按钮悬停效果增强 */
.btn:hover {
  @apply transform -translate-y-1;
}

/* 渐变按钮动画 */
.bg-gradient-to-r {
  background-size: 200% auto;
  transition: all 0.3s ease;
}

.bg-gradient-to-r:hover {
  background-position: right center;
}
</style>

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