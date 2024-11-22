<template>
  <div class="p-6">
    <!-- 用户信息区域 -->
    <div class="flex items-center space-x-6 mb-8">
      <!-- 用户头像 -->
      <div class="avatar placeholder">
        <div class="bg-neutral text-neutral-content rounded-full w-24">
          <span class="text-3xl">{{ username?.charAt(0).toUpperCase() }}</span>
        </div>
      </div>
      
      <!-- 用户统计信息 -->
      <div class="flex-1">
        <h2 class="text-2xl font-bold mb-2">{{ username }}</h2>
        <div class="stats shadow">
          <div class="stat">
            <div class="stat-title">批改总数</div>
            <div class="stat-value">{{ essayCount }}</div>
          </div>
          <div class="stat">
            <div class="stat-title">注册时间</div>
            <div class="stat-value text-base">{{ formatDate(createdAt) }}</div>
          </div>
        </div>
      </div>
      
      <!-- 修改密码按钮 -->
      <button class="btn btn-primary" @click="showPasswordDialog">
        修改密码
      </button>
    </div>

    <!-- 修改密码对话框 -->
    <dialog id="password_modal" class="modal">
      <div class="modal-box">
        <h3 class="font-bold text-lg mb-4">修改密码</h3>
        
        <form @submit.prevent="changePassword">
          <!-- 错误提示 -->
          <div v-if="error" class="alert alert-error mb-4">
            <span>{{ error }}</span>
            <button type="button" class="btn btn-ghost btn-xs" @click="error = null">关闭</button>
          </div>

          <!-- 成功提示 -->
          <div v-if="successMessage" class="alert alert-success mb-4">
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
              class="input input-bordered" 
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
              class="input input-bordered" 
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
              class="input input-bordered" 
              required
              :disabled="loading"
            />
          </div>
          
          <div class="modal-action">
            <button 
              type="submit" 
              class="btn btn-primary" 
              :disabled="loading || !isFormValid"
            >
              {{ loading ? '修改中...' : '确认修改' }}
            </button>
            <button type="button" class="btn" @click="closePasswordDialog">取消</button>
          </div>
        </form>
      </div>
      <form method="dialog" class="modal-backdrop">
        <button>关闭</button>
      </form>
    </dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import http from '../utils/axios'
import { authStore } from '../stores/auth'

export default {
  name: 'Profile',
  setup() {
    const currentPassword = ref('')
    const newPassword = ref('')
    const confirmPassword = ref('')
    const loading = ref(false)
    const error = ref(null)
    const successMessage = ref(null)
    const username = ref('')
    const essayCount = ref(0)
    const createdAt = ref(null)

    // 表单验证
    const isFormValid = computed(() => {
      return currentPassword.value.trim() !== '' && 
             newPassword.value.trim() !== '' && 
             confirmPassword.value.trim() !== ''
    })

    const fetchUserInfo = async () => {
      try {
        loading.value = true
        const response = await http.get(`/users/${authStore.userId}`)
        username.value = response.data.username
        essayCount.value = response.data.essay_count
        createdAt.value = response.data.created_at
      } catch (err) {
        console.error('获取用户信息失败:', err)
      } finally {
        loading.value = false
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
      error.value = null
      successMessage.value = null

      if (newPassword.value !== confirmPassword.value) {
        error.value = '两次输入的密码不一致'
        return
      }

      if (newPassword.value.length < 6) {
        error.value = '新密码长度不能小于6位'
        return
      }
      
      try {
        loading.value = true
        await http.post('/auth/change-password', {
          current_password: currentPassword.value,
          new_password: newPassword.value
        })
        successMessage.value = '密码修改成功'
        setTimeout(() => {
          closePasswordDialog()
        }, 1500)
      } catch (err) {
        error.value = err.response?.data?.error || '密码修改失败'
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      fetchUserInfo()
    })
    
    return {
      currentPassword,
      newPassword,
      confirmPassword,
      loading,
      error,
      successMessage,
      username,
      essayCount,
      createdAt,
      formatDate,
      showPasswordDialog,
      closePasswordDialog,
      changePassword,
      isFormValid
    }
  }
}
</script> 