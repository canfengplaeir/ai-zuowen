<template>
  <div class="min-h-screen bg-base-200">
    <!-- Loading 遮罩 -->
    <div v-if="loading" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="loading loading-spinner loading-lg text-primary"></div>
    </div>

    <!-- Toast 组件 -->
    <Toast />

    <!-- Confirm 对话框 -->
    <ConfirmDialog />

    <!-- 路由视图 -->
    <router-view></router-view>
  </div>
</template>

<script>
import { ref } from 'vue'
import Toast from './components/Toast.vue'
import ConfirmDialog from './components/ConfirmDialog.vue'

export default {
  components: {
    Toast,
    ConfirmDialog
  },
  
  setup() {
    const loading = ref(false)

    return {
      loading
    }
  }
}
</script> 