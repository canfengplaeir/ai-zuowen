<template>
  <div class="p-4 md:p-6 pt-20 md:pt-6">
    <!-- 顶部统计卡片 -->
    <div class="stats shadow w-full mb-6 flex-col md:flex-row">
      <div class="stat">
        <div class="stat-figure text-primary">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <div class="stat-title">总批改数</div>
        <div class="stat-value text-primary">{{ totalEssays }}</div>
        <div class="stat-desc">所有批改记录</div>
      </div>
      
      <div class="stat">
        <div class="stat-figure text-secondary">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
        </div>
        <div class="stat-title">本月批改</div>
        <div class="stat-value text-secondary">{{ monthlyEssays }}</div>
        <div class="stat-desc">{{ currentMonth }}月份</div>
      </div>
      
      <div class="stat">
        <div class="stat-figure text-accent">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
          </svg>
        </div>
        <div class="stat-title">平均分数</div>
        <div class="stat-value text-accent">{{ averageScore }}</div>
        <div class="stat-desc">总体表现</div>
      </div>
    </div>

    <!-- 搜索和筛选栏 -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
      <!-- 搜索框 -->
      <div class="w-full md:w-auto md:flex-1 max-w-md">
        <div class="form-control">
          <div class="input-group">
            <input 
              type="text" 
              placeholder="搜索作文内容、评语或分数..." 
              class="input input-bordered w-full" 
              v-model="searchQuery"
              @input="handleSearch"
            />
            <button class="btn btn-square" @click="clearSearch" v-if="searchQuery">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
            <button class="btn btn-square" v-else>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
      
      <!-- 筛选选项 -->
      <div class="flex flex-col sm:flex-row gap-2 w-full md:w-auto">
        <!-- 分数筛选 -->
        <select class="select select-bordered w-full sm:w-auto" v-model="filterScore" @change="handleSearch">
          <option value="all">所有分数</option>
          <option value="excellent">优秀 (90-100)</option>
          <option value="good">良好 (80-89)</option>
          <option value="average">中等 (70-79)</option>
          <option value="pass">及格 (60-69)</option>
          <option value="fail">不及格 (<60)</option>
        </select>
        
        <!-- 排序方式 -->
        <select class="select select-bordered w-full sm:w-auto" v-model="sortBy">
          <option value="date">按日期排序</option>
          <option value="score">按分数排序</option>
        </select>
        
        <!-- 分页按钮组 -->
        <div class="btn-group justify-center sm:justify-start">
          <button 
            class="btn btn-sm md:btn-md" 
            :disabled="currentPage === 1"
            @click="changePage(currentPage - 1)"
          >
            «
          </button>
          <button class="btn btn-sm md:btn-md">第 {{ currentPage }} / {{ totalPages }} 页</button>
          <button 
            class="btn btn-sm md:btn-md" 
            :disabled="currentPage === totalPages"
            @click="changePage(currentPage + 1)"
          >
            »
          </button>
        </div>
      </div>
    </div>

    <!-- 历史记录网格 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <!-- 无数据提示 -->
      <div v-if="filteredEssays.length === 0" class="col-span-full text-center py-12">
        <div class="flex flex-col items-center gap-6">
          <div class="w-24 h-24 rounded-full bg-base-200 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-base-content/30" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <div class="space-y-2">
            <p class="text-lg font-medium text-base-content/70">暂无批改记录</p>
            <p class="text-sm text-base-content/50">开始批改你的第一篇作文吧</p>
          </div>
          <router-link to="/app/english-essay" class="btn btn-primary">
            去批改作文
          </router-link>
        </div>
      </div>
      
      <!-- 作文卡片 -->
      <div v-else v-for="essay in filteredEssays" :key="essay.id" 
           class="card bg-base-100 hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
        <div class="card-body p-4 md:p-6">
          <!-- 卡片头部 -->
          <div class="flex justify-between items-start mb-4">
            <div class="flex items-center gap-2">
              <div class="badge badge-primary">英语作文</div>
              <div class="radial-progress text-primary" 
                   :style="{ '--value': essay.score || 0, '--size': '2.5rem', '--thickness': '2px' }">
                {{ essay.score }}
              </div>
            </div>
            <div class="text-sm text-base-content/60">
              {{ formatDate(essay.created_at) }}
            </div>
          </div>
          
          <!-- 作文内容预览 -->
          <div class="prose prose-sm max-w-none mb-4">
            <div class="font-english text-base-content/80 line-clamp-3 whitespace-pre-wrap">
              {{ truncateText(essay.content, 150) }}
            </div>
          </div>
          
          <!-- 总体评价预览 -->
          <div class="prose prose-sm max-w-none mb-4">
            <div class="text-base-content/70 line-clamp-2">
              {{ essay.feedback?.overall_feedback }}
            </div>
          </div>
          
          <!-- 操作按钮 -->
          <div class="card-actions justify-end mt-auto pt-2">
            <button class="btn btn-error btn-sm" @click.stop="confirmDelete(essay.id)">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              <span class="hidden md:inline ml-1">删除</span>
            </button>
            <button class="btn btn-primary btn-sm" @click.stop="showDetails(essay)">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              <span class="hidden md:inline ml-1">查看详情</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 详情模态框 -->
    <dialog id="essay_details" class="modal" @click="handleModalClick">
      <div class="modal-box w-11/12 max-w-5xl p-0 overflow-hidden" @click.stop>
        <!-- 固定的顶部栏 -->
        <div class="sticky top-0 bg-base-100 z-10 px-6 py-4 border-b flex justify-between items-center">
          <div class="flex items-center gap-4">
            <h3 class="font-bold text-lg">作文详情</h3>
            <span class="text-sm text-base-content/60">
              {{ selectedEssay?.created_at ? formatDate(selectedEssay.created_at) : '' }}
            </span>
          </div>
          <div class="flex items-center gap-2">
            <button 
              class="btn btn-ghost btn-sm tooltip tooltip-left" 
              data-tip="复制全文"
              @click="copyContent"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
            </button>
            <form method="dialog">
              <button class="btn btn-ghost btn-sm btn-circle">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </form>
          </div>
        </div>

        <!-- 可滚动的内容区域 -->
        <div class="p-6 overflow-y-auto max-h-[calc(90vh-4rem)] space-y-8">
          <!-- 原文内容 -->
          <div class="result-section">
            <h4 class="text-lg font-medium mb-4 flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              原文内容
            </h4>
            <div class="bg-base-200 p-6 rounded-lg shadow-lg">
              <p class="whitespace-pre-wrap font-english leading-relaxed">{{ selectedEssay?.content }}</p>
            </div>
          </div>

          <!-- 分数显示 -->
          <div class="result-section">
            <h4 class="text-lg font-medium mb-4 flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              得分评估
            </h4>
            <div class="flex items-center gap-6 bg-base-200 p-6 rounded-lg shadow-lg">
              <div class="radial-progress text-primary" :style="{ '--value': selectedEssay?.score || 0, '--size': '8rem', '--thickness': '8px' }">
                {{ selectedEssay?.score }}
              </div>
              <div class="space-y-2">
                <div class="text-xl font-medium" :class="{
                  'text-success': selectedEssay?.score >= 90,
                  'text-primary': selectedEssay?.score >= 80 && selectedEssay?.score < 90,
                  'text-warning': selectedEssay?.score >= 60 && selectedEssay?.score < 80,
                  'text-error': selectedEssay?.score < 60
                }">
                  {{ getScoreLevel(selectedEssay?.score) }}
                </div>
                <div class="text-base-content/70 text-sm">
                  {{ getScoreDescription(selectedEssay?.score) }}
                </div>
              </div>
            </div>
          </div>

          <!-- 批改结果部分 -->
          <div class="result-section">
            <h4 class="text-lg font-medium mb-4 flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              批改详情
            </h4>
            <div class="space-y-6">
              <!-- 总体评价 -->
              <div class="bg-base-200 p-6 rounded-lg shadow-lg">
                <h5 class="text-base font-medium mb-3 flex items-center gap-2">
                  <span class="badge badge-primary">总体评价</span>
                </h5>
                <p class="leading-relaxed">{{ selectedEssay?.feedback?.overall_feedback }}</p>
              </div>

              <!-- 语法问题 -->
              <div v-if="selectedEssay?.feedback?.grammar_issues?.length" class="bg-base-200 p-6 rounded-lg shadow-lg">
                <h5 class="text-base font-medium mb-4 flex items-center gap-2">
                  <span class="badge badge-primary">语法问题</span>
                </h5>
                <div class="space-y-4">
                  <div v-for="(issue, index) in selectedEssay.feedback.grammar_issues" 
                       :key="index" 
                       class="bg-base-100 p-4 rounded-lg">
                    <div class="flex flex-col gap-3">
                      <div class="flex items-start gap-2">
                        <span class="badge badge-error badge-sm">错误</span>
                        <p class="font-english">{{ issue.error }}</p>
                      </div>
                      <div class="flex items-start gap-2">
                        <span class="badge badge-success badge-sm">修改</span>
                        <p class="font-english">{{ issue.correction }}</p>
                      </div>
                      <div class="flex items-start gap-2 text-base-content/70">
                        <span class="badge badge-ghost badge-sm">说明</span>
                        <p>{{ issue.explanation }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 词汇反馈 -->
              <div v-if="selectedEssay?.feedback?.vocabulary_feedback" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="bg-base-200 p-6 rounded-lg shadow-lg">
                  <h5 class="text-base font-medium mb-3 flex items-center gap-2">
                    <span class="badge badge-success">亮点用词</span>
                  </h5>
                  <ul class="space-y-2">
                    <li v-for="(word, index) in selectedEssay.feedback.vocabulary_feedback.highlights" 
                        :key="index"
                        class="flex items-center gap-2">
                      <span class="text-success">•</span>
                      <span class="font-english">{{ word }}</span>
                    </li>
                  </ul>
                </div>
                <div class="bg-base-200 p-6 rounded-lg shadow-lg">
                  <h5 class="text-base font-medium mb-3 flex items-center gap-2">
                    <span class="badge badge-warning">建议改进</span>
                  </h5>
                  <ul class="space-y-2">
                    <li v-for="(suggestion, index) in selectedEssay.feedback.vocabulary_feedback.suggestions" 
                        :key="index"
                        class="flex items-center gap-2">
                      <span class="text-warning">•</span>
                      <span class="font-english">{{ suggestion }}</span>
                    </li>
                  </ul>
                </div>
              </div>

              <!-- 改进建议 -->
              <div v-if="selectedEssay?.feedback?.improvement_suggestions?.length" class="bg-base-200 p-6 rounded-lg shadow-lg">
                <h5 class="text-base font-medium mb-3 flex items-center gap-2">
                  <span class="badge badge-primary">改进建议</span>
                </h5>
                <ul class="space-y-3">
                  <li v-for="(suggestion, index) in selectedEssay.feedback.improvement_suggestions" 
                      :key="index"
                      class="flex items-start gap-3">
                    <span class="text-primary font-medium">{{ index + 1 }}.</span>
                    <span>{{ suggestion }}</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <form method="dialog" class="modal-backdrop">
        <button>关闭</button>
      </form>
    </dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject, nextTick, onUnmounted } from 'vue'
import http from '../utils/axios'
import { authStore } from '../stores/auth'
import { marked } from 'marked'
import { useToast } from '../components/Toast.vue'
import { useConfirm } from './ConfirmDialog.vue'
import Cropper from 'cropperjs'

const essays = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const loading = ref(false)
const selectedEssay = ref(null)
const searchQuery = ref('')
const searchTimeout = ref(null)
const sortBy = ref('date')
const filterScore = ref('all')  // 添加分数过滤
const totalEssays = ref(0)
const monthlyEssays = ref(0)
const averageScore = ref(0)

const currentMonth = computed(() => {
  return new Date().getMonth() + 1
})

const filteredEssays = computed(() => {
  let result = [...essays.value]
  
  // 搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(essay => 
      essay.content.toLowerCase().includes(query) ||
      essay.feedback?.overall_feedback?.toLowerCase().includes(query) ||
      String(essay.score).includes(query)
    )
  }
  
  // 分数过滤
  if (filterScore.value !== 'all') {
    result = result.filter(essay => {
      const score = essay.score || 0
      switch (filterScore.value) {
        case 'excellent': return score >= 90
        case 'good': return score >= 80 && score < 90
        case 'average': return score >= 70 && score < 80
        case 'pass': return score >= 60 && score < 70
        case 'fail': return score < 60
        default: return true
      }
    })
  }
  
  // 排序
  result.sort((a, b) => {
    if (sortBy.value === 'date') {
      return new Date(b.created_at) - new Date(a.created_at)
    } else if (sortBy.value === 'score') {
      return (b.score || 0) - (a.score || 0)
    }
    return 0
  })
  
  return result
})

const toast = useToast()
const confirm = useConfirm()
const setLoading = inject('setLoading')

const getImageUrl = async (userId, filename) => {
  try {
    // 移除多余的 /api 前缀，因为 axios 已经配置了 baseURL
    const response = await http.get(`/essay/image/${userId}/${filename}`, {
      responseType: 'blob'
    })
    return URL.createObjectURL(response.data)
  } catch (err) {
    console.error('获取图片失败:', err)
    return '' // 返回空字符串表示加载失败
  }
}

const fetchEssays = async () => {
  setLoading(true, '加载历史记录中...')
  try {
    const response = await http.get(`/essay/list/${authStore.userId}`, {
      params: { page: currentPage.value }
    })
    
    // 处理每个作文的图片
    const essaysWithImages = await Promise.all(
      response.data.essays.map(async essay => ({
        ...essay,
        // 移除多余的 /api 前缀
        image_url: await getImageUrl(essay.user_id, essay.original_image)
      }))
    )
    
    essays.value = essaysWithImages
    totalPages.value = response.data.total_pages
    totalEssays.value = response.data.total
    
    // 计算统计数据
    const now = new Date()
    monthlyEssays.value = essays.value.filter(essay => {
      const essayDate = new Date(essay.created_at)
      return essayDate.getMonth() === now.getMonth()
    }).length
    
    const scores = essays.value.map(essay => essay.score).filter(score => score)
    averageScore.value = scores.length ? 
      Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : 0
  } catch (err) {
    toast.error('获取历史记录失败')
  } finally {
    setLoading(false)
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const truncateText = (text, length = 100) => {
  if (text.length <= length) return text
  return text.slice(0, length) + '...'
}

const handleSearch = () => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }
  
  searchTimeout.value = setTimeout(async () => {
    setLoading(true, '搜索中...')
    try {
      currentPage.value = 1
      await fetchEssays()
    } finally {
      setLoading(false)
    }
  }, 300)  // 300ms 的防抖延迟
}

const clearSearch = () => {
  searchQuery.value = ''
  filterScore.value = 'all'
  sortBy.value = 'date'
  handleSearch()
}

const changePage = async (page) => {
  currentPage.value = page
  await fetchEssays()
}

const confirmDelete = async (essayId) => {
  const confirmed = await confirm.showConfirm(
    '删除记录',
    '确定要删除这条记录吗？删除后将无法恢复。'
  )
  
  if (confirmed) {
    try {
      setLoading(true, '删除中...')
      await http.delete(`/essay/${essayId}`)
      await fetchEssays()
      toast.success('删除成功')
    } catch (err) {
      toast.error('删除失败')
    } finally {
      setLoading(false)
    }
  }
}

const showDetails = (essay) => {
  selectedEssay.value = essay
  document.getElementById('essay_details').showModal()
}

const formattedFeedback = computed(() => {
  if (!selectedEssay.value?.feedback) return ''
  const markdownText = selectedEssay.value.feedback
    .replace(/【(.+?)】/g, '\n## $1\n')
    .replace(/\n/g, '\n\n')
  return marked(markdownText)
})

const getScoreLevel = (score) => {
  if (!score) return '未评分';
  if (score >= 90) return '优秀';
  if (score >= 80) return '良好';
  if (score >= 70) return '中等';
  if (score >= 60) return '及格';
  return '需要改进';
}

// 获取分数描述
const getScoreDescription = (score) => {
  if (!score) return '暂无评分'
  if (score >= 90) return '你的作文表现出色，继续保持！'
  if (score >= 80) return '你的作文水平不错，还有提升空间。'
  if (score >= 70) return '你的作文基本合格，需要更多练习。'
  if (score >= 60) return '你的作文刚刚及格，要加强训练。'
  return '你的作文需要更多努力，不要灰心。'
}

// 处理模态框点击
const handleModalClick = (e) => {
  if (e.target.classList.contains('modal')) {
    document.getElementById('essay_details').close()
  }
}

// 复制内容
const copyContent = async () => {
  if (!selectedEssay.value) return

  // 构建要复制的文本
  const content = [
    '作文内容：',
    selectedEssay.value.content,
    '\n得分：' + selectedEssay.value.score,
    '\n总体评价：',
    selectedEssay.value.feedback.overall_feedback,
    '\n语法问题：',
    ...(selectedEssay.value.feedback.grammar_issues || []).map(
      issue => `- ${issue.error}\n  修改：${issue.correction}\n  说明：${issue.explanation}`
    ),
    '\n词汇亮点：',
    ...(selectedEssay.value.feedback.vocabulary_feedback?.highlights || []).map(word => `- ${word}`),
    '\n词汇建议：',
    ...(selectedEssay.value.feedback.vocabulary_feedback?.suggestions || []).map(sugg => `- ${sugg}`),
    '\n结构优点：',
    ...(selectedEssay.value.feedback.structure_analysis?.strengths || []).map(str => `- ${str}`),
    '\n结构不足：',
    ...(selectedEssay.value.feedback.structure_analysis?.weaknesses || []).map(weak => `- ${weak}`),
    '\n改进建议：',
    ...(selectedEssay.value.feedback.improvement_suggestions || []).map((sugg, i) => `${i + 1}. ${sugg}`)
  ].join('\n')

  try {
    await navigator.clipboard.writeText(content)
    toast.success('内容已复制到剪贴板')
  } catch (err) {
    toast.error('复制失败，请手动复制')
    console.error('复制失败:', err)
  }
}

// 初始化裁剪器
const initCropper = () => {
  // 确保图片元素存在
  if (!cropperImage.value) {
    console.error('cropperImage element not found')
    return
  }

  // 销毁已存在的裁剪器实例
  if (cropper.value) {
    cropper.value.destroy()
    cropper.value = null
  }

  // 等待图片加载完成后再初始化裁剪器
  const img = cropperImage.value
  if (img.complete) {
    // 如果图片已经加载完成，直接初始化
    createCropper()
  } else {
    // 如果图片还在加载，等待加载完成后初始化
    img.onload = () => {
      createCropper()
    }
  }
}

// 创建裁剪器
const createCropper = () => {
  try {
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
        // 初始化完成后，设置裁剪框大小
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
    console.error('创建裁剪器失败:', err)
    toast.error('创建裁剪器失败，请重试')
  }
}

// 处理文件选择
const handleFileSelect = (event) => {
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

    // 使用 nextTick 确保 DOM 更新后再初始化裁剪器
    nextTick(() => {
      // 添加延迟以确保图片加载
      setTimeout(() => {
        initCropper()
      }, 100)
    })
  }
}

// 处理拍照上传
const handleCameraCapture = (blob) => {
  if (blob) {
    selectedFile.value = new File([blob], 'camera.jpg', { type: 'image/jpeg' })
    imageUrl.value = URL.createObjectURL(blob)
    step.value = 2

    // 使用 nextTick 确保 DOM 更新后再初始化裁剪器
    nextTick(() => {
      // 添加延迟以确保图片加载
      setTimeout(() => {
        initCropper()
      }, 100)
    })
  }
}

onMounted(() => {
  fetchEssays()
})

// 组件卸载时清理 blob URLs
onUnmounted(() => {
  essays.value.forEach(essay => {
    if (essay.image_url && essay.image_url.startsWith('blob:')) {
      URL.revokeObjectURL(essay.image_url)
    }
  })
})
</script>

<style scoped>
.prose :deep(h2) {
  @apply text-xl font-bold mt-4 mb-2;
}
.prose :deep(p) {
  @apply my-2;
}
.radial-progress {
  --size: 4rem;
  --thickness: 4px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .stats {
    @apply text-sm gap-2;
  }
  
  .stat {
    @apply p-4;
  }
  
  .stat-figure svg {
    @apply h-6 w-6;
  }
  
  .stat-value {
    @apply text-xl;
  }

  .btn-group {
    @apply w-full;
  }

  .btn-group .btn {
    @apply flex-1;
  }
}

.prose ul {
  @apply list-disc list-inside;
}

.prose li {
  @apply my-1;
}

.prose h4 {
  @apply text-lg font-medium mb-2;
}

.prose h5 {
  @apply text-base font-medium mb-2;
}

/* 英文字体优化 */
.font-english {
  font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.6;
  letter-spacing: 0.2px;
}

/* 反馈部分样式 */
.feedback-section {
  @apply bg-base-100 rounded-lg;
}

/* 滚动条美化 */
.modal-box ::-webkit-scrollbar {
  width: 6px;
}

.modal-box ::-webkit-scrollbar-track {
  @apply bg-base-200 rounded-full;
}

.modal-box ::-webkit-scrollbar-thumb {
  @apply bg-base-300 rounded-full hover:bg-base-content/20;
}

/* 搜索框动画 */
.input {
  @apply transition-all duration-200;
}

.input:focus {
  @apply transform scale-[1.02];
}

/* 筛选选项动画 */
.select {
  @apply transition-all duration-200;
}

.select:focus {
  @apply transform scale-[1.02];
}

/* 卡片动画 */
.card {
  @apply transform transition-all duration-300 hover:shadow-lg;
}

.card:hover {
  @apply -translate-y-1;
}

/* 移动端优化 */
@media (max-width: 768px) {
  .stats {
    @apply text-sm gap-2;
  }
  
  .stat {
    @apply p-4;
  }
  
  .stat-figure svg {
    @apply h-6 w-6;
  }
  
  .stat-value {
    @apply text-xl;
  }

  .btn-group {
    @apply w-full;
  }

  .btn-group .btn {
    @apply flex-1;
  }
  
  .card-body {
    @apply p-4;
  }
  
  .prose {
    @apply text-sm;
  }
}

/* 英文字体优化 */
.font-english {
  font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.6;
  letter-spacing: 0.2px;
}

/* 文本截断 */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 按钮动画 */
.btn {
  @apply transition-all duration-200;
}

.btn:hover {
  @apply transform scale-105;
}

/* 渐变加载动画 */
.loading-shimmer {
  background: linear-gradient(
    90deg,
    rgba(255,255,255,0) 0%,
    rgba(255,255,255,0.2) 50%,
    rgba(255,255,255,0) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}
</style> 