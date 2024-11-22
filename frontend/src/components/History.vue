<template>
  <div class="p-6">
    <!-- 顶部统计卡片 -->
    <div class="stats shadow w-full mb-6">
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
    <div class="flex justify-between items-center mb-6">
      <div class="flex-1 max-w-md">
        <div class="form-control">
          <div class="input-group">
            <input 
              type="text" 
              placeholder="搜索作文内容..." 
              class="input input-bordered w-full" 
              v-model="searchQuery"
              @input="handleSearch"
            />
            <button class="btn btn-square">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
      
      <div class="flex gap-2">
        <select class="select select-bordered" v-model="sortBy">
          <option value="date">按日期排序</option>
          <option value="score">按分数排序</option>
        </select>
        <div class="btn-group">
          <button 
            class="btn" 
            :disabled="currentPage === 1"
            @click="changePage(currentPage - 1)"
          >
            «
          </button>
          <button class="btn">第 {{ currentPage }} / {{ totalPages }} 页</button>
          <button 
            class="btn" 
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
      <div v-if="filteredEssays.length === 0" class="col-span-full text-center py-8">
        <div class="flex flex-col items-center gap-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p class="text-gray-500">暂无批改记录</p>
        </div>
      </div>
      
      <div v-else v-for="essay in filteredEssays" :key="essay.id" 
           class="card bg-base-100 hover:shadow-lg transition-shadow">
        <div class="card-body">
          <div class="flex justify-between items-start">
            <div class="badge badge-primary">英语作文</div>
            <div class="text-sm text-gray-500">
              {{ formatDate(essay.created_at) }}
            </div>
          </div>
          
          <div class="divider my-2">原文预览</div>
          <p class="text-sm whitespace-pre-wrap max-h-24 overflow-y-auto">
            {{ truncateText(essay.content) }}
          </p>
          
          <div class="divider my-2">得分</div>
          <div class="flex justify-center">
            <div class="radial-progress text-primary" :style="{ '--value': essay.score || 0, '--size': '4rem' }">
              {{ essay.score !== null ? essay.score : '未评分' }}
            </div>
          </div>
          
          <div class="card-actions justify-end mt-4">
            <button class="btn btn-error btn-sm" @click="confirmDelete(essay.id)">
              删除
            </button>
            <button class="btn btn-primary btn-sm" @click="showDetails(essay)">
              查看详情
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 详情模态框 -->
    <dialog id="essay_details" class="modal">
      <div class="modal-box w-11/12 max-w-5xl">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-bold text-lg">作文详情</h3>
          <span class="text-sm text-gray-500">
            {{ selectedEssay?.created_at ? formatDate(selectedEssay.created_at) : '' }}
          </span>
        </div>
        
        <div class="divider">原文</div>
        <div class="bg-base-200 p-4 rounded-lg">
          <p class="whitespace-pre-wrap">{{ selectedEssay?.content }}</p>
        </div>
        
        <div class="divider">批改意见</div>
        <div class="prose max-w-none bg-base-200 p-4 rounded-lg" v-html="formattedFeedback"></div>
        
        <div class="modal-action">
          <form method="dialog">
            <button class="btn">关闭</button>
          </form>
        </div>
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
import { marked } from 'marked'
import { useToast } from '../components/Toast.vue'
import { useConfirm } from './ConfirmDialog.vue'

export default {
  name: 'History',
  setup() {
    const essays = ref([])
    const currentPage = ref(1)
    const totalPages = ref(1)
    const loading = ref(false)
    const selectedEssay = ref(null)
    const searchQuery = ref('')
    const sortBy = ref('date')
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
          essay.content.toLowerCase().includes(query)
        )
      }
      
      // 排序
      result.sort((a, b) => {
        if (sortBy.value === 'date') {
          return new Date(b.created_at) - new Date(a.created_at)
        } else {
          return (b.score || 0) - (a.score || 0)
        }
      })
      
      return result
    })

    const toast = useToast()
    const confirm = useConfirm()

    const fetchEssays = async () => {
      try {
        loading.value = true
        const response = await http.get(`/essays/${authStore.userId}`, {
          params: { page: currentPage.value }
        })
        essays.value = response.data.essays
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
        loading.value = false
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
      currentPage.value = 1
      fetchEssays()
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
          loading.value = true
          await http.delete(`/essays/${essayId}`)
          await fetchEssays()
          toast.success('删除成功')
        } catch (err) {
          toast.error('删除失败')
        } finally {
          loading.value = false
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

    onMounted(() => {
      fetchEssays()
    })

    return {
      essays,
      currentPage,
      totalPages,
      loading,
      selectedEssay,
      searchQuery,
      sortBy,
      totalEssays,
      monthlyEssays,
      averageScore,
      currentMonth,
      filteredEssays,
      formattedFeedback,
      formatDate,
      truncateText,
      handleSearch,
      changePage,
      confirmDelete,
      showDetails
    }
  }
}
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
</style> 