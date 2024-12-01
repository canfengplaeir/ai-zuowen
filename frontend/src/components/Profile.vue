<template>
  <div class="p-4 md:p-6 pt-20 md:pt-6">
    <!-- 个人信息卡片 -->
    <div class="card bg-base-100 shadow-lg mb-6">
      <div class="card-body">
        <h3 class="card-title mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          个人资料
        </h3>
        
        <div class="space-y-4">
          <!-- 用户名 -->
          <div class="flex items-center gap-4">
            <div class="stat-title">用户名</div>
            <div class="stat-value text-lg">{{ userInfo.username }}</div>
          </div>

          <!-- 注册时间 -->
          <div class="flex items-center gap-4">
            <div class="stat-title">注册时间</div>
            <div class="stat-value text-lg">{{ formatDate(userInfo.created_at) }}</div>
          </div>

          <!-- 作文数量 -->
          <div class="flex items-center gap-4">
            <div class="stat-title">作文数量</div>
            <div class="stat-value text-lg">{{ userInfo.essay_count }}</div>
          </div>

          <!-- 修改密码按钮 -->
          <div class="flex justify-end">
            <button class="btn btn-primary" @click="showPasswordDialog">
              修改密码
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 修改密码对话框 -->
    <dialog id="password_modal" class="modal">
      <div class="modal-box w-11/12 max-w-md">
        <h3 class="font-bold text-lg mb-4">修改密码</h3>
        
        <form @submit.prevent="changePassword" class="space-y-4">
          <!-- 错误提示 -->
          <div v-if="error" class="alert alert-error">
            <span>{{ error }}</span>
            <button type="button" class="btn btn-ghost btn-xs" @click="error = null">关闭</button>
          </div>

          <!-- 成功提示 -->
          <div v-if="successMessage" class="alert alert-success">
            <span>{{ successMessage }}</span>
            <button type="button" class="btn btn-ghost btn-xs" @click="successMessage = null">关闭</button>
          </div>
          
          <div class="form-control">
            <label class="label">
              <span class="label-text">当前密码</span>
            </label>
            <input 
              type="password" 
              v-model="currentPassword" 
              class="input input-bordered w-full" 
              required
              :disabled="loading"
            />
          </div>
          
          <div class="form-control">
            <label class="label">
              <span class="label-text">新密码</span>
            </label>
            <input 
              type="password" 
              v-model="newPassword" 
              class="input input-bordered w-full" 
              required
              :disabled="loading"
            />
          </div>
          
          <div class="form-control">
            <label class="label">
              <span class="label-text">确认新密码</span>
            </label>
            <input 
              type="password" 
              v-model="confirmPassword" 
              class="input input-bordered w-full" 
              required
              :disabled="loading"
            />
          </div>
          
          <div class="modal-action flex-col md:flex-row gap-2">
            <button 
              type="submit" 
              class="btn btn-primary w-full md:w-auto" 
              :disabled="loading || !isFormValid"
            >
              {{ loading ? '修改中...' : '确认修改' }}
            </button>
            <button type="button" class="btn w-full md:w-auto" @click="closePasswordDialog">取消</button>
          </div>
        </form>
      </div>
      <form method="dialog" class="modal-backdrop">
        <button>关闭</button>
      </form>
    </dialog>

    <!-- 添加激活码区域 -->
    <div class="card bg-base-100 shadow-lg mb-6">
      <div class="card-body">
        <h3 class="card-title mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
          </svg>
          激活码
        </h3>
        
        <div class="space-y-4">
          <!-- 剩余次数显示 -->
          <div class="flex items-center gap-4">
            <div class="stat-title">剩余批改次数</div>
            <div class="stat-value text-primary">{{ userInfo.remaining_corrections || 0 }}</div>
          </div>

          <!-- 激活码输入 -->
          <div class="form-control">
            <div class="input-group">
              <input 
                type="text" 
                v-model="activationCode"
                placeholder="请输入激活码" 
                class="input input-bordered flex-1"
                :disabled="activating"
              />
              <button 
                class="btn btn-primary" 
                @click="activateCode"
                :disabled="!activationCode || activating"
              >
                {{ activating ? '激活中...' : '激活' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue'
import http from '../utils/axios'
import { authStore } from '../stores/auth'
import { useToast } from '../components/Toast.vue'

const toast = useToast()
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref(null)
const successMessage = ref(null)
const username = ref('')
const essayCount = ref(0)
const createdAt = ref(null)
const isAdmin = ref(false)
const activationCode = ref('')
const activating = ref(false)

const userInfo = ref({
  username: '',
  essay_count: 0,
  created_at: null,
  is_admin: false,
  remaining_corrections: 0
})

// 表单验证
const isFormValid = computed(() => {
  return currentPassword.value.trim() !== '' && 
         newPassword.value.trim() !== '' && 
         confirmPassword.value.trim() !== ''
})

const setLoading = inject('setLoading')

const fetchUserInfo = async () => {
  setLoading(true, '加载用户信息...')
  try {
    const response = await http.get('/auth/user/profile')
    userInfo.value = response.data
  } catch (err) {
    toast.error('获取用户信息失败')
  } finally {
    setLoading(false)
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}
  
const showPasswordDialog = () => {
  document.getElementById('password_modal').showModal()
}

const closePasswordDialog = () => {
  document.getElementById('password_modal').close()
  currentPassword.value = ''
  newPassword.value = ''
  confirmPassword.value = ''
  error.value = null
  successMessage.value = null
}
  
const changePassword = async () => {
  if (!currentPassword.value || !newPassword.value || !confirmPassword.value) {
    toast.warning('请填写所有密码字段')
    return
  }

  if (newPassword.value !== confirmPassword.value) {
    toast.warning('两次输入的新密码不一致')
    return
  }

  try {
    loading.value = true
    await http.put('/auth/user/password', {
      currentPassword: currentPassword.value,
      newPassword: newPassword.value
    })
    
    // 修改成功后的处理
    toast.success('密码修改成功')
    closePasswordDialog()  // 关闭对话框
    // 重置表单
    currentPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
    error.value = null
    successMessage.value = null
    
  } catch (err) {
    // 修改失败的处理
    const errorMessage = err.response?.data?.error || '修改密码失败'
    toast.error(errorMessage)
    error.value = errorMessage
    successMessage.value = null
  } finally {
    loading.value = false
  }
}

const activateCode = async () => {
  if (!activationCode.value) {
    toast.warning('请输入激活码')
    return
  }

  try {
    activating.value = true
    const response = await http.post('/activation/activate', {
      code: activationCode.value
    })

    toast.success(response.data.message)
    // 更新用户信息
    await fetchUserInfo()
    // 清空输入框
    activationCode.value = ''
  } catch (err) {
    toast.error(err.response?.data?.error || '激活失败')
  } finally {
    activating.value = false
  }
}

onMounted(() => {
  fetchUserInfo()
})
  
</script> 

<style scoped>
/* 响应式调整 */
@media (max-width: 768px) {
  .stats {
    @apply text-sm;
  }
  
  .stat-value {
    @apply text-xl;
  }
  
  .modal-box {
    @apply p-4;
    max-height: 90vh;
  }
}

/* 动画效果 */
.modal-box {
  @apply transition-all duration-300;
}

.input:focus {
  @apply transform scale-[1.02] transition-all duration-200;
}

.btn {
  @apply transition-all duration-200;
}

.btn:not(:disabled):hover {
  @apply transform -translate-y-0.5;
}

.stat-title {
  @apply text-base-content/60 text-sm;
}

.stat-value {
  @apply text-base-content font-medium;
}
</style> 