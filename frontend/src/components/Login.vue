<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="card bg-base-100 shadow-xl max-w-md w-full mx-4">
      <div class="card-body">
        <h2 class="card-title">{{ isRegister ? '注册' : '登录' }}</h2>
        <form @submit.prevent="handleAuth">
          <div class="form-control">
            <label class="label">
              <span class="label-text">用户名</span>
            </label>
            <input 
              type="text" 
              v-model="username" 
              class="input input-bordered" 
              required
              :disabled="loading"
            />
          </div>
          <div class="form-control">
            <label class="label">
              <span class="label-text">密码</span>
            </label>
            <input 
              type="password" 
              v-model="password" 
              class="input input-bordered" 
              required
              :disabled="loading"
            />
          </div>
          <div class="card-actions justify-end mt-4">
            <button 
              type="submit" 
              class="btn btn-primary" 
              :disabled="loading"
            >
              {{ loading ? '处理中...' : (isRegister ? '注册' : '登录') }}
            </button>
            <button 
              type="button"
              class="btn btn-link" 
              @click="isRegister = !isRegister"
              :disabled="loading"
            >
              {{ isRegister ? '已有账号？去登录' : '没有账号？去注册' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authStore } from '../stores/auth'
import http from '../utils/axios'
import { useToast } from '../components/Toast.vue'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const toast = useToast()
    const isRegister = ref(false)
    const username = ref('')
    const password = ref('')
    const loading = ref(false)

    const handleAuth = async () => {
      try {
        loading.value = true
        const endpoint = isRegister.value ? '/auth/register' : '/auth/login'
        const response = await http.post(endpoint, {
          username: username.value,
          password: password.value
        })
        
        if (!isRegister.value && response.data.token) {
          authStore.setAuth(response.data.token, response.data.user_id)
          toast.success('登录成功')
          router.push('/app/english-essay')
        } else if (isRegister.value) {
          isRegister.value = false
          toast.success('注册成功，请登录')
          username.value = ''
          password.value = ''
        }
      } catch (err) {
        toast.error(err.response?.data?.error || '操作失败')
      } finally {
        loading.value = false
      }
    }

    return {
      isRegister,
      username,
      password,
      loading,
      handleAuth
    }
  }
}
</script>

<style scoped>
.card {
  @apply transition-shadow duration-300;
}

.card:hover {
  @apply shadow-2xl;
}

.form-control {
  @apply mb-4;
}

.btn-link {
  @apply hover:no-underline;
}
</style> 