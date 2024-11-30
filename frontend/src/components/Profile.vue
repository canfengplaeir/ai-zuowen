<template>
  <div class="p-4 md:p-6 pt-20 md:pt-6">
    <!-- 用户信息区域 -->
    <div class="flex flex-col md:flex-row md:items-center gap-6 mb-8">
      <!-- 用户头像 -->
      <div class="avatar placeholder">
        <div class="bg-neutral text-neutral-content rounded-full w-20 md:w-24">
          <span class="text-2xl md:text-3xl">{{ username?.charAt(0).toUpperCase() }}</span>
        </div>
      </div>
      
      <!-- 用户统计信息 -->
      <div class="flex-1">
        <div class="flex items-center gap-2 mb-4">
          <h2 class="text-xl md:text-2xl font-bold">{{ username }}</h2>
          <!-- 用户角色标签 -->
          <div 
            :class="[
              'badge', 
              isAdmin ? 'badge-primary' : 'badge-secondary',
              'badge-lg'
            ]"
          >
            {{ isAdmin ? '管理员' : '用户' }}
          </div>
        </div>
        <div class="stats shadow w-full flex-col md:flex-row">
          <div class="stat">
            <div class="stat-title">批改总数</div>
            <div class="stat-value text-lg md:text-2xl">{{ essayCount }}</div>
          </div>
          <div class="stat">
            <div class="stat-title">注册时间</div>
            <div class="stat-value text-base">{{ formatDate(createdAt) }}</div>
          </div>
        </div>
      </div>
      
      <!-- 修改密码按钮 -->
      <div class="w-full md:w-auto">
        <button class="btn btn-primary w-full md:w-auto" @click="showPasswordDialog">
          修改密码
        </button>
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
    username.value = response.data.username
    essayCount.value = response.data.essay_count
    createdAt.value = response.data.created_at
    isAdmin.value = response.data.is_admin
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
    day: '2-digit'
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
</style> 