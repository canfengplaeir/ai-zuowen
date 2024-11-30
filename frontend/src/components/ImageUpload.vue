<template>
  <div class="flex flex-col gap-4">
    <!-- 拍照/上传按钮 -->
    <div class="flex gap-4">
      <label class="btn btn-primary">
        <input
          type="file"
          accept="image/*"
          capture="environment"
          class="hidden"
          @change="handleImageSelect"
        />
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        拍照上传
      </label>

      <label class="btn btn-secondary">
        <input
          type="file"
          accept="image/*"
          class="hidden"
          @change="handleImageSelect"
        />
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
        </svg>
        选择图片
      </label>
    </div>

    <!-- 预览区域 -->
    <div v-if="previewUrl" class="relative">
      <img :src="previewUrl" alt="预览" class="max-w-full h-auto rounded-lg shadow-lg" />
      <button 
        @click="clearImage" 
        class="btn btn-circle btn-sm absolute top-2 right-2 bg-base-100/80 hover:bg-base-200"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- 错误提示 -->
    <div v-if="error" class="alert alert-error">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <span>{{ error }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { authStore } from '../stores/auth'
import http from '../utils/axios'

const emit = defineEmits(['upload-success'])

const previewUrl = ref('')
const error = ref('')
const loading = ref(false)

const handleImageSelect = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  // 验证文件类型
  if (!file.type.startsWith('image/')) {
    error.value = '请选择图片文件'
    return
  }

  // 验证文件大小（最大 10MB）
  if (file.size > 10 * 1024 * 1024) {
    error.value = '图片大小不能超过10MB'
    return
  }

  try {
    // 清除之前的错误
    error.value = ''
    loading.value = true

    // 创建预览
    previewUrl.value = URL.createObjectURL(file)

    // 创建 FormData
    const formData = new FormData()
    formData.append('image', file)

    // 上传图片
    const response = await http.post('/essays/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Bearer ${authStore.token}`
      }
    })

    // 发送成功事件
    emit('upload-success', {
      content: response.data.content,
      imagePath: response.data.image_path
    })

  } catch (err) {
    console.error('上传错误:', err)
    error.value = err.response?.data?.error || '上传失败，请重试'
    clearImage()
  } finally {
    loading.value = false
  }
}

const clearImage = () => {
  previewUrl.value = ''
  error.value = ''
  // 重置 input
  const inputs = document.querySelectorAll('input[type="file"]')
  inputs.forEach(input => input.value = '')
}
</script> 