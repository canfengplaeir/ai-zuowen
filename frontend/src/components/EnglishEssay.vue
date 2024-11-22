<template>
  <div class="max-w-4xl mx-auto">
    <div class="card bg-base-100 shadow-xl">
      <div class="card-body">
        <h2 class="card-title mb-6">英语作文批改</h2>
        
        <!-- 步骤指示器 -->
        <ul class="steps w-full mb-8">
          <li class="step" :class="{ 'step-primary': step >= 1 }">选择图片</li>
          <li class="step" :class="{ 'step-primary': step >= 2 }">调整图片</li>
          <li class="step" :class="{ 'step-primary': step >= 3 }">批改结果</li>
        </ul>

        <!-- 步骤1: 选择图片 -->
        <div v-if="step === 1">
          <!-- 上传方式选择 -->
          <div v-if="!showCamera" class="grid grid-cols-2 gap-4">
            <!-- 本地上传 -->
            <label class="flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-lg cursor-pointer hover:bg-base-200 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span class="text-lg font-medium mb-2">本地上传</span>
              <span class="text-sm text-gray-500">点击或拖拽图片到此处</span>
              <input 
                type="file" 
                class="hidden" 
                @change="handleFileUpload"
                accept=".jpg,.jpeg,.png"
                :disabled="loading"
              />
            </label>

            <!-- 拍照上传 -->
            <button 
              class="flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-lg hover:bg-base-200 transition-colors"
              @click="startCamera"
              :disabled="loading"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <span class="text-lg font-medium mb-2">拍照上传</span>
              <span class="text-sm text-gray-500">使用摄像头拍摄</span>
            </button>
          </div>

          <!-- 相机拍摄区域 -->
          <div v-if="showCamera" class="mt-6 space-y-4">
            <!-- 相机选择 -->
            <div class="form-control">
              <select 
                class="select select-bordered w-full" 
                v-model="selectedCamera"
                @change="switchCamera"
              >
                <option value="">默认相机</option>
                <option v-for="camera in cameras" :key="camera.deviceId" :value="camera.deviceId">
                  {{ camera.label || `相机 ${cameras.indexOf(camera) + 1}` }}
                </option>
              </select>
            </div>

            <!-- 相机预览 -->
            <div class="relative aspect-video bg-black rounded-lg overflow-hidden">
              <video 
                ref="videoRef" 
                class="w-full h-full object-cover"
                autoplay 
                playsinline
                muted
              ></video>
              <div class="absolute inset-0 flex items-center justify-center" v-if="cameraLoading">
                <div class="loading loading-spinner loading-lg text-primary"></div>
              </div>
              <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex gap-4">
                <button 
                  class="btn btn-circle btn-error"
                  @click="cancelCamera"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
                <button 
                  class="btn btn-circle btn-primary"
                  @click="takePhoto"
                  :disabled="loading || cameraLoading"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 步骤2: 调整图片 -->
        <div v-if="step === 2" class="space-y-4">
          <div class="bg-base-200 rounded-lg overflow-hidden">
            <div class="cropper-container">
              <img 
                ref="cropperImage" 
                :src="imageUrl" 
                v-show="imageUrl"
                class="max-w-full"
              >
            </div>
            <div class="flex justify-between gap-4 p-4 bg-base-100 border-t">
              <button class="btn btn-ghost" @click="resetCrop">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                重置裁剪
              </button>
              <div>
                <button class="btn mr-2" @click="resetImage">重新选择</button>
                <button class="btn btn-primary" @click="confirmCrop">确认并提交</button>
              </div>
            </div>
          </div>
        </div>

        <!-- 步骤3: 批改结果 -->
        <div v-if="step === 3" class="space-y-6">
          <!-- 原图预览 -->
          <div>
            <h3 class="text-lg font-medium mb-2">原文图片</h3>
            <img :src="previewUrl" alt="预览" class="max-w-full h-auto rounded-lg shadow-lg" />
          </div>

          <!-- 批改结果 -->
          <div v-if="result">
            <h3 class="text-lg font-medium mb-2">批改结果</h3>
            <div class="prose max-w-none bg-base-200 p-4 rounded-lg">
              <div v-html="formattedResult"></div>
            </div>
          </div>

          <!-- 加载中状态 -->
          <div v-if="loading" class="text-center py-8">
            <div class="loading loading-spinner loading-lg"></div>
            <p class="mt-4 text-gray-500">正在批改中，请稍候...</p>
          </div>

          <!-- 底部按钮 -->
          <div class="flex justify-end gap-4">
            <button class="btn" @click="resetAll">重新批改</button>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onUnmounted, watch } from 'vue'
import http from '../utils/axios'
import { authStore } from '../stores/auth'
import { marked } from 'marked'
import { useToast } from '../components/Toast.vue'
import Cropper from 'cropperjs'
import 'cropperjs/dist/cropper.css'
import { useRouter } from 'vue-router'

export default {
  name: 'EnglishEssay',
  setup() {
    const toast = useToast()
    const selectedFile = ref(null)
    const previewUrl = ref('')
    const loading = ref(false)
    const result = ref('')
    const uploadMethod = ref('local')
    const videoRef = ref(null)
    const stream = ref(null)
    const imageUrl = ref('')
    const cropperImage = ref(null)
    const cropper = ref(null)
    const cameras = ref([])
    const selectedCamera = ref('')
    const step = ref(1)
    const showCamera = ref(false)
    const cameraLoading = ref(false)
    const router = useRouter()

    const formattedResult = computed(() => {
      if (!result.value) return ''
      const markdownText = result.value
        .replace(/【(.+?)】/g, '\n## $1\n')
        .replace(/\n/g, '\n\n')
      return marked(markdownText)
    })

    const initCropper = () => {
      if (cropperImage.value) {
        // 销毁之前的裁剪实例
        if (cropper.value) {
          cropper.value.destroy()
        }

        // 建新的裁剪实例
        cropper.value = new Cropper(cropperImage.value, {
          viewMode: 2,  // 限制裁剪框不超出图片的范围
          dragMode: 'move',
          aspectRatio: NaN,
          autoCropArea: 0.98,  // 初始裁剪框更大
          restore: false,
          modal: true,
          guides: true,
          highlight: true,
          cropBoxMovable: true,
          cropBoxResizable: true,
          toggleDragModeOnDblclick: true,
          minContainerWidth: 200,
          minContainerHeight: 200,
          minCropBoxWidth: 100,
          minCropBoxHeight: 100,
          background: true,
          movable: true,
          rotatable: false,
          scalable: true,
          zoomable: true,
          zoomOnTouch: true,
          zoomOnWheel: true,
          wheelZoomRatio: 0.1,
          ready() {
            // 初始化完成后，确保裁剪框最大化
            cropper.value.setCropBoxData({
              width: cropper.value.getContainerData().width * 0.98,
              height: cropper.value.getContainerData().height * 0.98
            })
          }
        })
      }
    }

    const handleFileUpload = (event) => {
      const file = event.target.files[0]
      if (file) {
        if (file.size > 5 * 1024 * 1024) {
          toast.warning('文件大小不能超过5MB')
          event.target.value = ''
          return
        }
        selectedFile.value = file
        imageUrl.value = URL.createObjectURL(file)
        step.value = 2
        // 等待图片加载完成后初始化裁剪器
        setTimeout(initCropper, 100)
      }
    }

    const getCameras = async () => {
      try {
        // 先检查是否支持 mediaDevices API
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
          throw new Error('浏览器不支持访问摄像头')
        }

        // 请求相机权限
        const stream = await navigator.mediaDevices.getUserMedia({ video: true })
        // 立即停止这个测试流
        stream.getTracks().forEach(track => track.stop())

        // 获取设备列表
        const devices = await navigator.mediaDevices.enumerateDevices()
        cameras.value = devices.filter(device => device.kind === 'videoinput')
        
        // 如果没有找到相机设备
        if (cameras.value.length === 0) {
          throw new Error('未检测到可用的摄像头')
        }

        // 设置默认相机
        if (!selectedCamera.value) {
          // 优先选择后置相机
          const backCamera = cameras.value.find(camera => 
            camera.label.toLowerCase().includes('back') || 
            camera.label.toLowerCase().includes('后置') ||
            camera.label.toLowerCase().includes('rear')
          )
          selectedCamera.value = backCamera?.deviceId || cameras.value[0].deviceId
        }
      } catch (err) {
        console.error('获取相机列表失败:', err)
        toast.error(err.message || '无法访问相机')
        return false
      }
      return true
    }

    const startCamera = async () => {
      try {
        cameraLoading.value = true
        await stopCamera() // 确保先停止之前的相机

        // 获取相机列表
        const camerasAvailable = await getCameras()
        if (!camerasAvailable) {
          return
        }

        const constraints = {
          video: {
            deviceId: selectedCamera.value ? { exact: selectedCamera.value } : undefined,
            facingMode: selectedCamera.value ? undefined : 'environment',
            width: { ideal: 1920 },
            height: { ideal: 1080 }
          }
        }

        stream.value = await navigator.mediaDevices.getUserMedia(constraints)
        
        if (videoRef.value) {
          videoRef.value.srcObject = stream.value
          // 等待视频加载完成
          await new Promise((resolve, reject) => {
            const timeoutId = setTimeout(() => {
              reject(new Error('视频加载超时'))
            }, 5000) // 5秒超时

            videoRef.value.onloadedmetadata = () => {
              clearTimeout(timeoutId)
              videoRef.value.play().then(resolve).catch(reject)
            }
          })
        }
        
        showCamera.value = true
      } catch (err) {
        console.error('相机访问错误:', err)
        toast.error(err.message || '无法访问相机，请确保已授予相机权限')
        showCamera.value = false
      } finally {
        cameraLoading.value = false
      }
    }

    const switchCamera = async () => {
      try {
        cameraLoading.value = true
        await stopCamera()
        await startCamera()
      } finally {
        cameraLoading.value = false
      }
    }

    const stopCamera = async () => {
      try {
        if (stream.value) {
          const tracks = stream.value.getTracks()
          tracks.forEach(track => {
            track.stop()
            stream.value.removeTrack(track)
          })
          stream.value = null
        }
        if (videoRef.value) {
          videoRef.value.srcObject = null
        }
      } catch (err) {
        console.error('停止相机失败:', err)
      }
    }

    const takePhoto = () => {
      const video = videoRef.value
      if (!video) return

      const canvas = document.createElement('canvas')
      canvas.width = video.videoWidth
      canvas.height = video.videoHeight
      const ctx = canvas.getContext('2d')
      ctx.drawImage(video, 0, 0)
      
      canvas.toBlob((blob) => {
        if (blob) {
          selectedFile.value = new File([blob], "photo.jpg", { type: "image/jpeg" })
          imageUrl.value = URL.createObjectURL(blob)
          step.value = 2
          // 等待图片加载完成后初始化裁剪器
          setTimeout(initCropper, 100)
        }
      }, 'image/jpeg', 0.95)
      showCamera.value = false
    }

    const confirmCrop = async () => {
      if (cropper.value) {
        cropper.value.getCroppedCanvas({
          maxWidth: 1920,
          maxHeight: 1080,
          fillColor: '#fff',
        }).toBlob(
          async (blob) => {
            if (blob) {
              selectedFile.value = new File([blob], 'cropped.jpg', { type: 'image/jpeg' })
              previewUrl.value = URL.createObjectURL(blob)
              // 销毁裁剪实例
              cropper.value.destroy()
              cropper.value = null
              step.value = 3
              await uploadEssay()
            }
          },
          'image/jpeg',
          0.9
        )
      }
    }

    const resetImage = () => {
      if (cropper.value) {
        cropper.value.destroy()
        cropper.value = null
      }
      selectedFile.value = null
      imageUrl.value = ''
      previewUrl.value = ''
      result.value = ''
      step.value = 1
      showCamera.value = false
      stopCamera()
    }

    const uploadEssay = async () => {
      if (!selectedFile.value) {
        toast.warning('请选择文件')
        return
      }

      try {
        loading.value = true
        const formData = new FormData()
        formData.append('image', selectedFile.value)
        formData.append('user_id', authStore.userId)

        const response = await http.post('/essay/upload', formData)

        if (response.data) {
          result.value = response.data.feedback
          toast.success('作文批改完成')
        }
      } catch (err) {
        toast.error(err.response?.data?.error || '上传失败')
      } finally {
        loading.value = false
      }
    }

    watch(uploadMethod, (newMethod, oldMethod) => {
      if (oldMethod === 'camera') {
        stopCamera()
      }
      if (newMethod === 'camera') {
        startCamera()
      }
    })

    // 在组件卸载时清理资源
    onUnmounted(() => {
      stopCamera()
      if (cropper.value) {
        cropper.value.destroy()
      }
      // 清理所有的 URL 对象
      if (imageUrl.value) {
        URL.revokeObjectURL(imageUrl.value)
      }
      if (previewUrl.value) {
        URL.revokeObjectURL(previewUrl.value)
      }
    })

    const resetAll = () => {
      step.value = 1
      showCamera.value = false
      stopCamera()
      resetImage()
      result.value = ''
    }

    const cancelCamera = () => {
      showCamera.value = false
      stopCamera()
    }

    // 添加重置裁剪方法
    const resetCrop = () => {
      if (cropper.value) {
        cropper.value.reset()
        // 重置后重新设置裁剪框大小
        setTimeout(() => {
          cropper.value.setCropBoxData({
            width: cropper.value.getContainerData().width * 0.98,
            height: cropper.value.getContainerData().height * 0.98
          })
        }, 0)
      }
    }

    // 监听步骤变化，确保在步骤改变时关闭相机
    watch(step, (newStep) => {
      if (newStep !== 1) {
        stopCamera()
        showCamera.value = false
      }
    })

    // 监听路由变化
    watch(() => router.currentRoute.value.path, () => {
      stopCamera()
    })

    return {
      selectedFile,
      previewUrl,
      loading,
      result,
      formattedResult,
      uploadMethod,
      videoRef,
      imageUrl,
      handleFileUpload,
      startCamera,
      switchCamera,
      takePhoto,
      confirmCrop,
      resetImage,
      uploadEssay,
      cameras,
      selectedCamera,
      cropperImage,
      initCropper,
      step,
      showCamera,
      resetAll,
      cancelCamera,
      resetCrop,
      cameraLoading
    }
  }
}
</script>

<style>
.prose {
  @apply text-base-content;
}
.prose h2 {
  @apply text-xl font-bold mt-4 mb-2;
}
.prose p {
  @apply my-2;
}
.cropper-container {
  width: 100%;
  height: 70vh; /* 使用视口高度而不是固定高度 */
  max-height: 800px;
  background: #000;
}
.cropper-view-box,
.cropper-face {
  border-radius: 0;
}
.cropper-container img {
  max-width: 100%;
  max-height: 100%;
}
.cropper-line,
.cropper-point {
  background-color: var(--primary);
}
.cropper-view-box {
  outline: 2px solid var(--primary);
}
.modal-box {
  max-height: 90vh;
  overflow-y: auto;
}
.cropper-container {
  width: 100%;
  height: 500px;
  background: #000;
}
.cropper-view-box,
.cropper-face {
  border-radius: 0;
}
.cropper-line {
  background-color: var(--primary);
  opacity: 0.6;
}
.cropper-point {
  width: 12px;
  height: 12px;
  background-color: var(--primary);
  opacity: 0.8;
  border-radius: 50%; /* 使用圆形拖动点 */
  border: 2px solid #fff; /* 添加白色边框 */
}
.cropper-point.point-e,
.cropper-point.point-n,
.cropper-point.point-w,
.cropper-point.point-s {
  width: 10px;
  height: 10px;
}
.cropper-point.point-ne,
.cropper-point.point-nw,
.cropper-point.point-sw,
.cropper-point.point-se {
  width: 14px;
  height: 14px;
  background-color: var(--primary);
  opacity: 1;
}
.cropper-point.point-se {
  width: 16px;
  height: 16px;
  background-color: var(--primary);
  opacity: 1;
}
.cropper-view-box {
  outline: 2px solid var(--primary);
  outline-color: rgba(var(--primary), 0.75);
  box-shadow: 0 0 0 1px #fff inset; /* 添加内部白色边框 */
}
.cropper-face {
  background-color: transparent;
  cursor: move;
}
.cropper-face::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 24px;
  height: 24px;
  background-color: var(--primary);
  opacity: 0.5;
  border-radius: 50%;
  pointer-events: none;
}
.cropper-modal {
  background-color: rgba(0, 0, 0, 0.7);
}
.cropper-dashed {
  border-color: #fff;
  opacity: 0.3;
}

/* 添加拖放区域样式 */
.border-dashed {
  border-style: dashed;
  border-width: 2px;
  border-color: var(--base-content);
  opacity: 0.3;
}

.border-dashed:hover {
  opacity: 0.5;
}

/* 添加过渡效果 */
.cropper-view-box,
.cropper-face,
.cropper-line,
.cropper-point {
  transition: all 0.1s ease-out;
}

/* 添加相机加载状态样式 */
.loading-spinner {
  width: 3rem;
  height: 3rem;
}
</style> 