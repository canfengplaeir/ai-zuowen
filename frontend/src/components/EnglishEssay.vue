<template>
  <div class="p-4 md:p-6 space-y-6 md:pt-6 pt-16">
    <div class="card bg-base-100 shadow-xl min-h-[calc(100vh-6rem)] md:min-h-0">
      <div class="card-body p-4 md:p-6">
        <h2 class="card-title mb-6">英语作文批改</h2>
        
        <!-- 步骤指示器 -->
        <ul class="steps steps-vertical lg:steps-horizontal w-full mb-8">
          <li class="step" :class="{ 'step-primary': step >= 1 }">选择图片</li>
          <li class="step" :class="{ 'step-primary': step >= 2 }">调整图片</li>
          <li class="step" :class="{ 'step-primary': step >= 3 }">批改结果</li>
        </ul>

        <!-- 步骤1: 选择图片 -->
        <div v-if="step === 1">
          <!-- 上传方式选择 -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- 本地上传 -->
            <label class="upload-card">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mb-4 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span class="text-lg font-medium mb-2">本地上传</span>
              <span class="text-sm text-base-content/60">点击或拖拽图片到此处</span>
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
              class="upload-card"
              @click="startCamera"
              :disabled="loading"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mb-4 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <span class="text-lg font-medium mb-2">拍照上传</span>
              <span class="text-sm text-base-content/60">使用摄像头拍摄</span>
            </button>
          </div>

          <!-- 桌面端相机界面 -->
          <div v-if="showCamera && !isMobile" class="camera-overlay">
            <!-- 相机控制栏 -->
            <div class="camera-header">
              <button class="btn btn-ghost btn-sm" @click="() => {
                showCamera = false;
                stopStream();
              }">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
              <h3 class="text-lg font-bold text-white">拍照上传</h3>
              <div class="w-6"></div>
            </div>

            <!-- 相机预览区域 -->
            <div class="camera-preview">
              <!-- 视频预览 -->
              <video
                ref="videoRef"
                class="camera-video"
                autoplay
                playsinline
              ></video>
              
              <!-- 网格辅助线 -->
              <div class="camera-grid">
                <div class="grid-line vertical"></div>
                <div class="grid-line vertical"></div>
                <div class="grid-line horizontal"></div>
                <div class="grid-line horizontal"></div>
              </div>
              
              <!-- 加载状态 -->
              <div v-if="cameraLoading" class="camera-loading">
                <div class="loading loading-spinner loading-lg text-primary"></div>
                <p class="mt-4 text-white text-sm">正在启动相机...</p>
              </div>
            </div>

            <!-- 相机控制区域 -->
            <div class="camera-controls">
              <!-- 相机选择 -->
              <div class="camera-select">
                <select 
                  class="select select-bordered select-sm w-full max-w-xs bg-opacity-50 text-white"
                  v-model="selectedCamera"
                  :disabled="cameraLoading"
                >
                  <option disabled value="">请选择摄像头</option>
                  <option 
                    v-for="camera in cameras" 
                    :key="camera.deviceId" 
                    :value="camera.deviceId"
                  >
                    {{ camera.label || `摄像头 ${cameras.indexOf(camera) + 1}` }}
                  </option>
                </select>
              </div>

              <!-- 拍照按钮 -->
              <div class="camera-footer">
                <button 
                  class="camera-button"
                  @click="takePhoto"
                  :disabled="!selectedCamera || cameraLoading"
                >
                  <div class="camera-button-inner"></div>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 步骤2: 调整图片 -->
        <div v-if="step === 2" class="space-y-4">
          <div class="cropper-container">
            <!-- 添加局部加载状态 -->
            <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-base-100/50 z-10">
              <div class="loading loading-spinner loading-lg text-primary"></div>
            </div>
            
            <div class="cropper-wrapper">
              <img 
                ref="cropperImage" 
                :src="imageUrl" 
                v-show="imageUrl"
                class="max-w-full"
              >
            </div>
            <div class="cropper-controls">
              <button class="btn btn-ghost" @click="resetCrop">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                重置裁剪
              </button>
              <div class="flex gap-2">
                <button class="btn" @click="resetImage">重新选择</button>
                <button class="btn btn-primary" @click="confirmCrop">确认并提交</button>
              </div>
            </div>
          </div>
        </div>

        <!-- 步骤3: 批改结果 -->
        <div v-if="step === 3" class="space-y-6">
          <!-- 原图预览 -->
          <div class="result-section">
            <h3 class="text-lg font-medium mb-2">原文图片</h3>
            <div class="bg-base-200 rounded-lg overflow-hidden">
              <div class="image-container">
                <img 
                  :src="previewUrl" 
                  alt="预览" 
                  class="w-full h-auto object-contain"
                />
              </div>
            </div>
          </div>

          <!-- 原文内容 -->
          <div class="result-section">
            <h3 class="text-lg font-medium mb-2">原文内容</h3>
            <div class="bg-base-200 p-4 rounded-lg">
              <p class="whitespace-pre-wrap">{{ content }}</p>
            </div>
          </div>

          <!-- 分数显示 -->
          <div v-if="score !== null" class="result-section">
            <h3 class="text-lg font-medium mb-2">得分</h3>
            <div class="flex justify-center">
              <div class="radial-progress text-primary" :style="{ '--value': score, '--size': '6rem' }">
                {{ score }}
              </div>
            </div>
          </div>

          <!-- 批改结果部分 -->
          <div v-if="result" class="result-section">
            <h3 class="text-lg font-medium mb-2">批改结果</h3>
            <div class="space-y-6 bg-base-200 p-4 rounded-lg">
              <!-- 总体评价 -->
              <div class="prose max-w-none">
                <h4 class="text-base font-medium">总体评价</h4>
                <p>{{ result.overall_feedback }}</p>
              </div>

              <!-- 语法问题 -->
              <div v-if="result.grammar_issues?.length" class="prose max-w-none">
                <h4 class="text-base font-medium">语法问题</h4>
                <div class="space-y-3">
                  <div v-for="(issue, index) in result.grammar_issues" :key="index" class="bg-base-100 p-3 rounded">
                    <p class="text-error">错误：{{ issue.error }}</p>
                    <p class="text-success">修改：{{ issue.correction }}</p>
                    <p class="text-base-content/70">说明：{{ issue.explanation }}</p>
                  </div>
                </div>
              </div>

              <!-- 词汇反馈 -->
              <div v-if="result.vocabulary_feedback" class="prose max-w-none">
                <h4 class="text-base font-medium">词汇运用</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <h5 class="text-sm font-medium text-success">亮点用词</h5>
                    <ul>
                      <li v-for="(word, index) in result.vocabulary_feedback.highlights" :key="index">
                        {{ word }}
                      </li>
                    </ul>
                  </div>
                  <div>
                    <h5 class="text-sm font-medium text-warning">建议改进</h5>
                    <ul>
                      <li v-for="(suggestion, index) in result.vocabulary_feedback.suggestions" :key="index">
                        {{ suggestion }}
                      </li>
                    </ul>
                  </div>
                </div>
              </div>

              <!-- 结构分析 -->
              <div v-if="result.structure_analysis" class="prose max-w-none">
                <h4 class="text-base font-medium">结构分析</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <h5 class="text-sm font-medium text-success">优点</h5>
                    <ul>
                      <li v-for="(strength, index) in result.structure_analysis.strengths" :key="index">
                        {{ strength }}
                      </li>
                    </ul>
                  </div>
                  <div>
                    <h5 class="text-sm font-medium text-warning">不足</h5>
                    <ul>
                      <li v-for="(weakness, index) in result.structure_analysis.weaknesses" :key="index">
                        {{ weakness }}
                      </li>
                    </ul>
                  </div>
                </div>
              </div>

              <!-- 改进建议 -->
              <div v-if="result.improvement_suggestions?.length" class="prose max-w-none">
                <h4 class="text-base font-medium">改进建议</h4>
                <ul>
                  <li v-for="(suggestion, index) in result.improvement_suggestions" :key="index">
                    {{ suggestion }}
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- 加载中状态 -->
          <div v-if="loading" class="loading-container">
            <div class="loading loading-spinner loading-lg text-primary"></div>
            <p class="mt-4 text-base-content/70">正在批改中，请稍候...</p>
          </div>

          <!-- 底部按钮 -->
          <div class="flex justify-end gap-4 mt-8">
            <button class="btn" @click="resetAll">重新批改</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 上传卡片样式 */
.upload-card {
  @apply flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-lg cursor-pointer hover:bg-base-200 transition-all duration-300;
}

.upload-card:hover {
  @apply border-primary transform scale-[1.02];
}

/* 相机界面样式优化 */
.camera-overlay {
  @apply fixed inset-0 bg-black z-50 flex flex-col;
}

.camera-header {
  @apply p-4 flex justify-between items-center bg-black bg-opacity-50 backdrop-blur-sm;
}

.camera-preview {
  @apply flex-1 relative bg-black;
}

.camera-video {
  @apply absolute inset-0 w-full h-full object-contain;
}

/* 网格辅助线 */
.camera-grid {
  @apply absolute inset-0 pointer-events-none;
}

.grid-line {
  @apply absolute bg-white bg-opacity-20;
}

.grid-line.vertical {
  @apply w-px h-full;
}

.grid-line.horizontal {
  @apply h-px w-full;
}

.grid-line.vertical:nth-child(1) {
  left: 33.33%;
}

.grid-line.vertical:nth-child(2) {
  right: 33.33%;
}

.grid-line.horizontal:nth-child(3) {
  top: 33.33%;
}

.grid-line.horizontal:nth-child(4) {
  bottom: 33.33%;
}

/* 相机控制区域 */
.camera-controls {
  @apply bg-black bg-opacity-50 backdrop-blur-sm p-4 space-y-4;
}

.camera-select {
  @apply flex justify-center;
}

.camera-select select {
  @apply bg-black bg-opacity-50 border-white border-opacity-20 text-white;
}

.camera-select select option {
  @apply bg-black text-white;
}

.camera-footer {
  @apply flex justify-center;
}

.camera-button {
  @apply btn btn-circle btn-lg bg-white hover:bg-gray-100 transition-all duration-200;
}

.camera-button-inner {
  @apply w-12 h-12 rounded-full border-4 border-primary transition-all duration-200;
}

.camera-button:hover .camera-button-inner {
  @apply border-primary/80 transform scale-95;
}

.camera-loading {
  @apply absolute inset-0 flex flex-col items-center justify-center bg-black bg-opacity-70 backdrop-blur-sm;
}

/* 加载动画 */
.loading-spinner {
  @apply text-white;
}

/* 裁剪区域样式 */
.cropper-container {
  @apply bg-base-200 rounded-lg overflow-hidden;
}

.cropper-wrapper {
  width: 100%;
  height: 70vh;
  max-height: 800px;
  background: #000;
}

.cropper-controls {
  @apply flex justify-between gap-4 p-4 bg-base-100 border-t;
}

/* 结果区域样式 */
.result-section {
  @apply space-y-2 animate-fade-in;
}

.section-title {
  @apply text-lg font-medium;
}

.result-image {
  @apply max-w-full h-auto rounded-lg shadow-lg;
}

.result-content {
  @apply prose max-w-none bg-base-200 p-4 rounded-lg;
}

.loading-container {
  @apply text-center py-8;
}

.loading-text {
  @apply mt-4 text-base-content/70;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .steps {
    @apply text-sm;
  }
  
  .card-body {
    @apply p-4;
  }

  .upload-card {
    @apply p-6;
  }

  .camera-button {
    @apply btn-md;
  }

  .camera-button-inner {
    @apply w-8 h-8;
  }

  .camera-select select {
    @apply text-sm;
  }

  .camera-video {
    @apply object-cover;
  }
}

/* 动画效果 */
.upload-card,
.btn,
.camera-button {
  @apply transition-all duration-200;
}

.upload-card:hover,
.btn:not(:disabled):hover,
.camera-button:not(:disabled):hover {
  @apply transform scale-[1.02];
}

/* Markdown 样式优化 */
.prose {
  @apply text-base-content;
}

:deep(.markdown-content) {
  /* 标题样式 */
  h1, h2, h3, h4, h5, h6 {
    @apply font-bold text-base-content mt-6 mb-4;
  }
  
  h1 { @apply text-2xl; }
  h2 { @apply text-xl; }
  h3 { @apply text-lg; }
  
  /* 段落样式 */
  p {
    @apply my-4 leading-relaxed;
  }
  
  /* 列表样式 */
  ul, ol {
    @apply my-4 pl-6;
  }
  
  ul {
    @apply list-disc;
  }
  
  ol {
    @apply list-decimal;
  }
  
  /* 引用样式 */
  blockquote {
    @apply pl-4 border-l-4 border-primary/30 italic my-4;
  }
  
  /* 代码样式 */
  code {
    @apply px-1 py-0.5 bg-base-300 rounded text-sm;
  }
  
  pre {
    @apply p-4 bg-base-300 rounded-lg overflow-x-auto my-4;
  }
  
  /* 强调样式 */
  strong {
    @apply font-bold text-primary;
  }
  
  em {
    @apply italic text-base-content/80;
  }
  
  /* 分隔线样式 */
  hr {
    @apply my-8 border-base-300;
  }
  
  /* 链接样式 */
  a {
    @apply text-primary hover:text-primary/80 underline;
  }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .card-body {
    @apply p-4;
  }
  
  .steps {
    @apply text-xs;
  }
  
  .prose {
    @apply text-sm;
  }
  
  :deep(.markdown-content) {
    h1 { @apply text-xl; }
    h2 { @apply text-lg; }
    h3 { @apply text-base; }
  }
}

/* 动画效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 加载状态样式 */
.loading-container {
  @apply flex flex-col items-center justify-center py-12;
}

.loading-spinner {
  @apply text-primary;
}

/* 结果区域样式 */
.result-section {
  @apply space-y-2 animate-fade-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out forwards;
}

/* 添加响应式图片容器样式 */
@media (min-width: 768px) {
  .max-w-xl {
    max-width: 36rem;  /* 约576px */
  }
  
  .aspect-w-4 {
    position: relative;
    padding-bottom: 75%;  /* 4:3 比例 */
  }
  
  .aspect-h-3 {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
  }
}

@media (max-width: 767px) {
  .max-w-xl {
    max-width: 100%;
  }
}

/* 添加图片容器样式 */
.image-container {
  @apply mx-auto;
  max-height: 200px; /* 限制图片高度为大约4-5行文字的高度 */
  overflow: hidden;
}

.image-container img {
  @apply w-full h-full object-contain;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .image-container {
    max-height: none; /* 移动端不限制高度 */
  }
}

/* 加载状态样式 */
.loading-container {
  @apply flex flex-col items-center justify-center py-12;
}

.loading-spinner {
  @apply text-primary;
}

/* 裁剪容器样式 */
.cropper-container {
  @apply relative;  /* 添加相对定位以支持绝对定位的加载状态 */
}

.prose ul {
  @apply list-disc list-inside;
}

.prose li {
  @apply my-1;
}
</style>

<script setup>
import { ref, computed, onUnmounted, watch, inject, nextTick } from 'vue'
import http from '../utils/axios'
import { authStore } from '../stores/auth'
import { useToast } from '../components/Toast.vue'
import Cropper from 'cropperjs'
import 'cropperjs/dist/cropper.css'
import { useRouter } from 'vue-router'
// 使用 markdown-it 替代 marked
import MarkdownIt from 'markdown-it'

// 初始化 markdown-it
const md = new MarkdownIt({
  html: true,
  breaks: true,
  linkify: true
})

// 获取设置加载状态的方法
const setLoading = inject('setLoading')

const toast = useToast()
const selectedFile = ref(null)
const previewUrl = ref('')
const loading = ref(false)
const result = ref('')
const content = ref('')  // 添加 content 响应式变量
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
const webcamRef = ref(null)
const score = ref(null)  // 添加 score ref

const formattedResult = computed(() => {
  if (!result.value) return ''
  
  // 处特殊标记
  let markdownText = result.value
    .replace(/【(.+?)】/g, '\n## $1\n')  // 将【】转换为二级标题
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')  // 保持粗体标记
    .replace(/\*(.+?)\*/g, '<em>$1</em>')  // 保持斜体标记
    .replace(/\n/g, '\n\n')  // 确保段落间有足够空行
  
  // 使用 markdown-it 转换
  return md.render(markdownText)
})

// 处理拍照上传
const handleCameraCapture = (blob) => {
  if (blob) {
    selectedFile.value = new File([blob], 'camera.jpg', { type: 'image/jpeg' })
    if (imageUrl.value) {
      URL.revokeObjectURL(imageUrl.value)
    }
    imageUrl.value = URL.createObjectURL(blob)
    step.value = 2

    // 使用 nextTick 确保 DOM 更新后再初始化裁剪器
    nextTick(() => {
      const img = cropperImage.value
      if (!img) {
        console.error('cropperImage element not found')
        return
      }

      // 等待图片加载
      const waitForImageLoad = () => {
        if (img.complete) {
          initCropper()
        } else {
          img.onload = initCropper
        }
      }

      waitForImageLoad()
    })
  }
}

// 初始化裁剪器
const initCropper = () => {
  try {
    if (cropper.value) {
      cropper.value.destroy()
    }

    cropper.value = new Cropper(cropperImage.value, {
      viewMode: 2,
      dragMode: 'move',
      aspectRatio: NaN,
      autoCropArea: 0.98,
      restore: false,
      modal: true,
      guides: true,
      highlight: true,
      cropBoxMovable: true,
      cropBoxResizable: true,
      toggleDragModeOnDblclick: true,
      ready() {
        if (cropper.value) {
          const containerData = cropper.value.getContainerData()
          cropper.value.setCropBoxData({
            width: containerData.width * 0.98,
            height: containerData.height * 0.98
          })
        }
      }
    })
  } catch (err) {
    console.error('初始化裁剪器失败:', err)
    toast.error('初始化裁剪器失败，请重试')
  }
}

// 处理文件选择
const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    if (!allowedTypes.includes(file.type)) {
      toast.error('不支持的文件类型')
      return
    }
    selectedFile.value = file
    // 创建新的图片 URL
    if (imageUrl.value) {
      URL.revokeObjectURL(imageUrl.value)
    }
    imageUrl.value = URL.createObjectURL(file)
    step.value = 2
    // 等待 DOM 更新后初始化裁剪器
    nextTick(() => {
      initCropper()
    })
  }
}

// 检查是否为移动设备
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)

// 启动相机
const startCamera = async () => {
  if (isMobile) {
    // 移动端：使用系统相机
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = 'image/*'
    input.capture = 'environment'  // 优先使用后置相机
    
    input.onchange = (event) => {
      const file = event.target.files[0]
      if (file) {
        handleCapturedImage(file)
      }
    }
    
    input.click()
  } else {
    // 桌面端：使用网页相机
    showCamera.value = true
    await initWebCamera()
  }
}

// 初始化网页相机
const initWebCamera = async () => {
  try {
    cameraLoading.value = true

    // 检查浏览器支持
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      throw new Error('您的浏览器不支持访问摄像头，请使用现代浏览器或选择本地上传')
    }

    // 获取相机列表
    const devices = await navigator.mediaDevices.enumerateDevices()
    cameras.value = devices.filter(device => device.kind === 'videoinput')

    if (cameras.value.length === 0) {
      throw new Error('未检测到可用的摄像头')
    }

    // 选择相机
    const savedCamera = localStorage.getItem('selectedCamera')
    selectedCamera.value = savedCamera && cameras.value.some(cam => cam.deviceId === savedCamera)
      ? savedCamera
      : cameras.value[0].deviceId

    await startStream()
  } catch (err) {
    console.error('相机初始化错误:', err)
    toast.error(err.message || '无法访问相机，请确保已授予相机权限')
    showCamera.value = false
  } finally {
    cameraLoading.value = false
  }
}

// 启动视频流
const startStream = async () => {
  try {
    if (stream.value) {
      stopStream()
    }

    const constraints = {
      video: {
        deviceId: selectedCamera.value ? { exact: selectedCamera.value } : undefined,
        width: { ideal: 1920 },
        height: { ideal: 1080 }
      }
    }

    stream.value = await navigator.mediaDevices.getUserMedia(constraints)
    
    if (videoRef.value) {
      videoRef.value.srcObject = stream.value
      await videoRef.value.play()
    }
  } catch (err) {
    console.error('启动视频流错误:', err)
    let errorMessage = '相机启动失败'
    
    // 根据错误类型提供具体的错误信息
    if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
      errorMessage = '无法访问相机，请确保已授予相机权限'
    } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
      errorMessage = '未找到可用的摄像头设备'
    } else if (err.name === 'NotReadableError' || err.name === 'TrackStartError') {
      errorMessage = '相机可能被其他应用程序占用，请关闭其他使用相机的应用'
    } else if (err.name === 'OverconstrainedError') {
      errorMessage = '相机不支持请求的分辨率，请尝试其他摄像头'
    }
    
    toast.error(errorMessage)
    throw err
  }
}

// 停止视频流
const stopStream = () => {
  if (stream.value) {
    stream.value.getTracks().forEach(track => track.stop())
    stream.value = null
  }
  if (videoRef.value) {
    videoRef.value.srcObject = null
  }
}

// 切换相机
const switchCamera = async () => {
  const currentIndex = cameras.value.findIndex(camera => camera.deviceId === selectedCamera.value)
  const nextIndex = (currentIndex + 1) % cameras.value.length
  selectedCamera.value = cameras.value[nextIndex].deviceId
  localStorage.setItem('selectedCamera', selectedCamera.value)
  await startStream()
}

// 拍照
const takePhoto = () => {
  if (!videoRef.value) return

  const canvas = document.createElement('canvas')
  canvas.width = videoRef.value.videoWidth
  canvas.height = videoRef.value.videoHeight
  
  const ctx = canvas.getContext('2d')
  ctx.drawImage(videoRef.value, 0, 0)
  
  canvas.toBlob((blob) => {
    if (blob) {
      handleCapturedImage(blob)
    }
  }, 'image/jpeg', 0.95)
}

// 处理捕获的图片
const handleCapturedImage = (blob) => {
  selectedFile.value = new File([blob], "photo.jpg", { type: "image/jpeg" })
  imageUrl.value = URL.createObjectURL(blob)
  step.value = 2
  showCamera.value = false
  stopStream()
  // 等待图片加载完成后初始化裁剪器
  setTimeout(initCropper, 100)
}

// 监听相机选择变化
watch(selectedCamera, async (newValue) => {
  if (newValue && !isMobile && showCamera.value) {
    try {
      cameraLoading.value = true
      await startStream()
    } catch (err) {
      toast.error('切换相机失败：' + (err.message || '未知错误'))
      // 切换相机失败时回退到之前的选择
      const previousCamera = cameras.value.find(cam => cam.deviceId !== newValue)
      if (previousCamera) {
        selectedCamera.value = previousCamera.deviceId
      }
    } finally {
      cameraLoading.value = false
    }
  }
})

// 关闭相机
const closeCamera = () => {
  showCamera.value = false
  stopStream()
}

// 监听相关状态变化
watch([
  () => router.currentRoute.value.path, // 路由变化
  step, // 步骤变化
  () => authStore.isLoggedIn, // 登录状态变化
], () => {
  closeCamera()
})

// 组件卸载时清理资源
onUnmounted(() => {
  closeCamera()
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

// 确认裁剪
const confirmCrop = async () => {
  if (!cropper.value) {
    console.error('Cropper not initialized')
    toast.error('裁剪器未初始化，请重新选择图片')
    return
  }

  try {
    loading.value = true  // 显示局部加载状态
    const canvas = cropper.value.getCroppedCanvas({
      maxWidth: 1920,
      maxHeight: 1080,
      fillColor: '#fff',
    })

    if (!canvas) {
      throw new Error('Failed to create canvas')
    }

    const blob = await new Promise((resolve, reject) => {
      canvas.toBlob(
        (b) => b ? resolve(b) : reject(new Error('Failed to create blob')),
        'image/jpeg',
        0.9
      )
    })

    selectedFile.value = new File([blob], 'cropped.jpg', { type: 'image/jpeg' })
    
    // 上传裁剪后的图片
    const uploadSuccess = await uploadEssay()
    if (uploadSuccess) {
      step.value = 3
    }
  } catch (err) {
    console.error('裁剪错误:', err)
    toast.error('图片处理失败，请重试')
  } finally {
    loading.value = false  // 关闭局部加载状态
  }
}

// 重置裁剪
const resetCrop = () => {
  if (cropper.value) {
    cropper.value.reset()
    // 重置后重新设置裁剪框大小
    const containerData = cropper.value.getContainerData()
    cropper.value.setCropBoxData({
      width: containerData.width * 0.98,
      height: containerData.height * 0.98
    })
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
  stopStream()
}

const uploadEssay = async () => {
  if (!selectedFile.value) {
    toast.warning('请选择文件')
    return false
  }

  try {
    loading.value = true
    const formData = new FormData()
    formData.append('file', selectedFile.value)

    const response = await http.post('/essay/upload', formData)

    if (response.data) {
      content.value = response.data.content
      result.value = response.data.feedback
      score.value = response.data.score
      
      if (response.data.image_path) {
        // 移除返回路径中的 /api 前缀
        const imagePath = response.data.image_path.replace(/^\/api/, '')
        const imageResponse = await http.get(imagePath, {
          responseType: 'blob'
        })
        previewUrl.value = URL.createObjectURL(imageResponse.data)
      }
      
      toast.success('作文批改完成')
      return true
    }
    return false
  } catch (err) {
    console.error('上传错误:', err)
    toast.error(err.response?.data?.error || '上传失败')
    return false
  } finally {
    loading.value = false
  }
}

watch(uploadMethod, (newMethod, oldMethod) => {
  if (oldMethod === 'camera') {
    stopStream()
  }
  if (newMethod === 'camera') {
    startCamera()
  }
})

const resetAll = () => {
  step.value = 1
  showCamera.value = false
  stopStream()
  resetImage()
  content.value = ''
  result.value = ''
  score.value = null
}

// 监听步骤变化，确保在步骤变时关闭相机
watch(step, (newStep) => {
  if (newStep !== 1) {
    stopStream()
    showCamera.value = false
  }
})

// 监听路由变化
watch(() => router.currentRoute.value.path, () => {
  stopStream()
})

const handleUpload = async () => {
  setLoading(true, '正在上传图片...')
  try {
    // ... 上传逻辑
  } finally {
    setLoading(false)
  }
}

// 添加允许的文件类型
const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png']
</script> 