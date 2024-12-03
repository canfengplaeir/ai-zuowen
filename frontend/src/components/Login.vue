<template>
  <div class="min-h-screen flex items-center justify-center bg-login relative">
    <!-- 背景遮罩 -->
    <div class="absolute inset-0 bg-black/40"></div>
    
    <!-- 登录卡片 -->
    <div class="card relative z-10 max-w-md w-full mx-4">
      <!-- 亚克力效果容器 -->
      <div class="acrylic absolute inset-0 rounded-2xl"></div>
      
      <!-- 卡片内容 -->
      <div class="card-body relative z-20">
        <!-- 卡片顶部装饰 -->
        <div class="absolute top-0 left-0 right-0 h-2 bg-gradient-to-r from-primary to-secondary animate-gradient rounded-t-2xl"></div>
        
        <div class="flex flex-col items-center mb-6">
          <div class="avatar placeholder mb-4">
            <div class="bg-gradient-to-r from-primary to-secondary text-primary-content rounded-lg w-16 h-16 animate-gradient">
              <span class="text-2xl">AI</span>
            </div>
          </div>
          <h2 class="card-title text-2xl font-bold">
            {{ isRegister ? '创建账号' : '欢迎回来' }}
          </h2>
        </div>

        <form @submit.prevent="handleAuth" class="space-y-4">
          <!-- 用户名输入框 -->
          <div class="form-control">
            <label class="label">
              <span class="label-text">用户名</span>
            </label>
            <input 
              type="text" 
              v-model="username" 
              class="input input-bordered w-full" 
              :disabled="loading"
              placeholder="请输入用户名"
            />
          </div>

          <!-- 密码输入框 -->
          <div class="form-control">
            <label class="label">
              <span class="label-text">密码</span>
            </label>
            <input 
              type="password" 
              v-model="password" 
              class="input input-bordered w-full" 
              :disabled="loading"
              placeholder="请输入密码"
            />
          </div>

          <!-- 注册时的额外选项 -->
          <template v-if="isRegister">
            <!-- 用户协议 -->
            <div class="flex items-center gap-2">
              <input 
                type="checkbox" 
                id="terms" 
                v-model="acceptTerms"
                class="checkbox checkbox-primary"
              />
              <label for="terms" class="text-sm">
                我已阅读并同意
                <router-link 
                  to="/terms" 
                  target="_blank"
                  class="text-primary hover:underline"
                >
                  《用户协议与隐私政策》
                </router-link>
              </label>
            </div>
          </template>

          <!-- 登录/注册按钮 -->
          <button 
            type="submit" 
            class="btn btn-primary w-full"
            :disabled="loading || (isRegister && !acceptTerms)"
          >
            {{ loading ? '处理中...' : (isRegister ? '注册' : '登录') }}
          </button>

          <!-- 切换登录/注册 -->
          <div class="text-center text-sm">
            <span class="text-base-content/70">
              {{ isRegister ? '已有账号？' : '还没有账号？' }}
            </span>
            <a 
              class="text-primary hover:underline cursor-pointer ml-1"
              @click="isRegister = !isRegister"
            >
              {{ isRegister ? '去登录' : '去注册' }}
            </a>
          </div>
        </form>
      </div>
    </div>

    <!-- 验证码弹窗 -->
    <dialog id="verify_modal" class="modal">
      <div class="modal-box max-w-[360px] p-6">
        <h3 class="font-bold text-lg mb-6 text-center">请完成人机验证</h3>
        
        <!-- 验证码组件 -->
        <div class="flex justify-center">
          <Vcode 
            :show="showVerify"
            @success="onVerifySuccess"
            @close="onVerifyClose"
            @reset="onVerifyReset"
          />
        </div>

        <div class="modal-action mt-6">
          <form method="dialog">
            <button class="btn btn-ghost">取消</button>
          </form>
        </div>
      </div>
    </dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authStore } from '../stores/auth'
import http from '../utils/axios'
import { useToast } from '../components/Toast.vue'
import Vcode from 'vue3-puzzle-vcode'

const router = useRouter()
const toast = useToast()
const showVerify = ref(false)
const isRegister = ref(false)
const username = ref('')
const password = ref('')
const loading = ref(false)
const acceptTerms = ref(false)

// 处理登录/注册
const handleAuth = async () => {
  if (!username.value || !password.value) {
    toast.warning('请输入用户名和密码')
    return
  }

  if (isRegister.value) {
    if (!acceptTerms.value) {
      toast.warning('请阅读并同意用户协议')
      return
    }
    showVerify.value = true
  } else {
    // 登录直接处理
    await processAuth()
  }
}

// 验证码成功回调
const onVerifySuccess = async () => {
  showVerify.value = false
  await processAuth()
}

// 验证码关闭回调
const onVerifyClose = () => {
  showVerify.value = false
}

// 验证码重置回调
const onVerifyReset = () => {
  console.log('验证码已刷新')
}

// 处理认证
const processAuth = async () => {
  try {
    loading.value = true
    const endpoint = isRegister.value ? '/auth/register' : '/auth/login'
    const response = await http.post(endpoint, {
      username: username.value,
      password: password.value
    })

    authStore.setAuth(response.data.token, response.data.user_id, response.data.is_admin)
    toast.success(isRegister.value ? '注册成功' : '登录成功')
    router.push('/app/english-essay')
  } catch (err) {
    toast.error(err.response?.data?.error || '操作失败')
  } finally {
    loading.value = false
    showVerify.value = false
  }
}
</script>

<style scoped>
.bg-login {
  background-image: url('https://objectstorageapi.bja.sealos.run/g6rnmc1y-mymy/hero-bg.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.card {
  @apply transition-all duration-300;
}

/* 渐变动画 */
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
  animation: gradient 3s linear infinite;
}

/* 其他动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out;
}

.animate-slide-up {
  animation: slideUp 0.5s ease-out;
}

.delay-300 {
  animation-delay: 300ms;
}

.delay-400 {
  animation-delay: 400ms;
}

/* 输入框样式 */
.input {
  @apply transition-all duration-200 rounded-xl;
}

.input:focus {
  @apply transform scale-[1.02];
}

/* 按钮样式 */
.btn {
  @apply transition-all duration-200 rounded-xl;
}

.btn:not(:disabled):hover {
  @apply transform scale-[1.02];
}

/* 卡片圆角和阴影 */
.card {
  @apply rounded-2xl overflow-hidden shadow-xl;
}

.card-body {
  @apply p-8;
}

/* 亚克力效果 */
.acrylic {
  backdrop-filter: 
    /* 背景模糊 */
    blur(16px)
    /* 亮度调整 */
    brightness(110%)
    /* 饱和度调整 */
    saturate(120%);
  
  /* 渐变背景 */
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.3) 0%,
    rgba(255, 255, 255, 0.2) 100%
  );
  
  /* 添加阴影 */
  box-shadow: 
    0 8px 32px 0 rgba(31, 38, 135, 0.2),
    inset 0 0 0 1px rgba(255, 255, 255, 0.1);
  
  /* 添加边框 */
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* 卡片内容样式优化 */
.card-body {
  @apply bg-transparent backdrop-blur-none;
}

/* 输入框样式优化 */
.input {
  @apply bg-white/40 backdrop-blur-sm border-white/20;
  transition: all 0.3s ease;
}

.input:focus {
  @apply bg-white/60 border-white/40;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* 按钮样式优化 */
.btn-primary {
  @apply bg-primary/90 backdrop-blur-sm hover:bg-primary;
  transition: all 0.3s ease;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* 动画效果 */
.card {
  @apply transition-all duration-500;
  animation: cardAppear 0.5s ease-out;
}

@keyframes cardAppear {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style> 