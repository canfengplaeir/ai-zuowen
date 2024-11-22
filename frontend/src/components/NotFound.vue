<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="text-center">
      <h1 class="text-8xl font-bold text-primary mb-4">404</h1>
      <p class="text-2xl mb-8">页面不存在</p>
      <router-link 
        :to="authStore.isAuthenticated() ? '/app/english-essay' : '/'" 
        class="btn btn-primary"
      >
        返回首页
      </router-link>
    </div>
  </div>
</template>

<script>
import { authStore } from '../stores/auth'

export default {
  name: 'NotFound',
  setup() {
    return {
      authStore
    }
  }
}
</script> 