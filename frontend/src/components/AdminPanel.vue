<template>
  <div class="p-4 md:p-6 pt-20 md:pt-6">
    <h2 class="text-2xl font-bold mb-6">管理员控制台</h2>
    
    <!-- 统计信息卡片 -->
    <div class="stats shadow w-full flex-col md:flex-row">
      <div class="stat">
        <div class="stat-title">总用户数</div>
        <div class="stat-value text-lg md:text-2xl">{{ stats.userCount }}</div>
      </div>
      <div class="stat">
        <div class="stat-title">总作文数</div>
        <div class="stat-value text-lg md:text-2xl">{{ stats.essayCount }}</div>
      </div>
      <div class="stat">
        <div class="stat-title">今日批改</div>
        <div class="stat-value text-lg md:text-2xl">{{ stats.todayCount }}</div>
      </div>
    </div>

    <!-- 标签页 -->
    <div class="tabs tabs-boxed flex">
      <a 
        class="tab flex-1 md:flex-none" 
        :class="{ 'tab-active': activeTab === 'users' }"
        @click="activeTab = 'users'"
      >
        用户管理
      </a>
      <a 
        class="tab flex-1 md:flex-none" 
        :class="{ 'tab-active': activeTab === 'essays' }"
        @click="activeTab = 'essays'"
      >
        作文管理
      </a>
      <a 
        class="tab flex-1 md:flex-none" 
        :class="{ 'tab-active': activeTab === 'codes' }"
        @click="activeTab = 'codes'"
      >
        激活码管理
      </a>
    </div>

    <!-- 用户管理 -->
    <div v-if="activeTab === 'users'" class="overflow-x-auto">
      <div class="overflow-x-auto">
        <table class="table w-full">
          <thead>
            <tr>
              <th class="hidden md:table-cell">ID</th>
              <th>用户名</th>
              <th class="hidden md:table-cell">注册时间</th>
              <th>作文数量</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td class="hidden md:table-cell">{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td class="hidden md:table-cell">{{ formatDate(user.created_at) }}</td>
              <td>{{ user.essay_count }}</td>
              <td>
                <button 
                  class="btn btn-error btn-xs"
                  @click="handleDeleteUser(user)"
                >
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 作文管理 -->
    <div v-if="activeTab === 'essays'" class="overflow-x-auto">
      <div class="overflow-x-auto">
        <table class="table w-full">
          <thead>
            <tr>
              <th class="hidden md:table-cell">ID</th>
              <th>用户</th>
              <th>分数</th>
              <th class="hidden md:table-cell">提交时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="essay in essays" :key="essay.id">
              <td class="hidden md:table-cell">{{ essay.id }}</td>
              <td>{{ essay.username }}</td>
              <td>{{ essay.score }}</td>
              <td class="hidden md:table-cell">{{ formatDate(essay.created_at) }}</td>
              <td>
                <button 
                  class="btn btn-primary btn-xs"
                  @click="viewEssay(essay)"
                >
                  查看
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 激活码管理 -->
    <div v-if="activeTab === 'codes'" class="space-y-6">
      <!-- 生成激活码表单 -->
      <div class="card bg-base-100 shadow">
        <div class="card-body">
          <h3 class="card-title">生成激活码</h3>
          <div class="flex flex-col md:flex-row gap-4">
            <div class="form-control">
              <label class="label">
                <span class="label-text">生成数量</span>
              </label>
              <input 
                type="number" 
                v-model="generateCount"
                class="input input-bordered" 
                min="1"
                max="100"
              />
            </div>
            <div class="form-control">
              <label class="label">
                <span class="label-text">批改次数</span>
              </label>
              <input 
                type="number" 
                v-model="correctionCount"
                class="input input-bordered" 
                min="1"
              />
            </div>
            <div class="form-control mt-8">
              <button 
                class="btn btn-primary"
                @click="generateCodes"
                :disabled="generating"
              >
                {{ generating ? '生成中...' : '生成激活码' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 激活码列表 -->
      <div class="overflow-x-auto">
        <table class="table w-full">
          <thead>
            <tr>
              <th>激活码</th>
              <th>批改次数</th>
              <th>状态</th>
              <th>使用者</th>
              <th>使用时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="code in activationCodes" :key="code.id">
              <td>{{ code.code }}</td>
              <td>{{ code.correction_count }}</td>
              <td>
                <span 
                  class="badge" 
                  :class="code.is_used ? 'badge-error' : 'badge-success'"
                >
                  {{ code.is_used ? '已使用' : '未使用' }}
                </span>
              </td>
              <td>{{ code.used_by_username || '-' }}</td>
              <td>{{ code.used_at ? formatDate(code.used_at) : '-' }}</td>
              <td>
                <button 
                  class="btn btn-error btn-xs"
                  @click="deleteCode(code.id)"
                  :disabled="code.is_used"
                >
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 作文详情对话框 -->
    <dialog id="essay_detail_modal" class="modal">
      <div class="modal-box w-11/12 max-w-5xl">
        <h3 class="font-bold text-lg mb-4">作文详情</h3>
        <div class="prose max-w-none">
          <div class="space-y-4">
            <div>
              <h4 class="font-bold">原文内容：</h4>
              <p class="whitespace-pre-wrap">{{ selectedEssay?.content }}</p>
            </div>
            <div>
              <h4 class="font-bold">批改意见：</h4>
              <div class="whitespace-pre-wrap" v-html="selectedEssay?.feedback"></div>
            </div>
            <div>
              <h4 class="font-bold">得分：</h4>
              <p>{{ selectedEssay?.score }}</p>
            </div>
          </div>
        </div>
        <div class="modal-action">
          <form method="dialog">
            <button class="btn">关闭</button>
          </form>
        </div>
      </div>
    </dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, inject } from 'vue'
import http from '../utils/axios'
import { useToast } from '../components/Toast.vue'
import { useConfirm } from '../components/ConfirmDialog.vue'

const toast = useToast()
const confirm = useConfirm()
const activeTab = ref('users')
const stats = reactive({
  userCount: 0,
  essayCount: 0,
  todayCount: 0
})
const users = ref([])
const essays = ref([])
const selectedEssay = ref(null)

const setLoading = inject('setLoading')

const fetchStats = async () => {
  setLoading(true, '加载统计信息...')
  try {
    const response = await http.get('/essay/admin/stats')
    Object.assign(stats, response.data)
  } catch (err) {
    toast.error('获取统计信息失败')
  } finally {
    setLoading(false)
  }
}

const fetchUsers = async () => {
  setLoading(true, '加载用户列表...')
  try {
    const response = await http.get('/admin/users')
    users.value = response.data
  } catch (err) {
    toast.error('获取用户列表失败')
  } finally {
    setLoading(false)
  }
}

const fetchEssays = async () => {
  setLoading(true, '加载作文列表...')
  try {
    const response = await http.get('/essay/admin/all')
    essays.value = response.data
  } catch (err) {
    toast.error('获取作文列表失败')
  } finally {
    setLoading(false)
  }
}

const handleDeleteUser = async (user) => {
  setLoading(true, '删除用户中...')
  const confirmed = await confirm.showConfirm(
    '删除用户',
    `确定要删除用户 "${user.username}" 吗？此操作不可恢复。`
  )
  
  if (confirmed) {
    try {
      await http.delete(`/admin/users/${user.id}`)
      await fetchUsers()
      await fetchStats()
      toast.success('用户删除成功')
    } catch (err) {
      toast.error(err.response?.data?.error || '删除用户失败')
    } finally {
      setLoading(false)
    }
  }
}

const viewEssay = (essay) => {
  selectedEssay.value = essay
  document.getElementById('essay_detail_modal').showModal()
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('zh-CN')
}

// 添加激活码相关的状态
const generateCount = ref(1)
const correctionCount = ref(10)
const generating = ref(false)
const activationCodes = ref([])

// 生成激活码
const generateCodes = async () => {
  if (generating.value) return
  
  try {
    generating.value = true
    const response = await http.post('/activation/generate', {
      count: generateCount.value,
      correction_count: correctionCount.value
    })
    
    toast.success(response.data.message)
    await fetchActivationCodes()
  } catch (err) {
    toast.error(err.response?.data?.error || '生成失败')
  } finally {
    generating.value = false
  }
}

// 获取激活码列表
const fetchActivationCodes = async () => {
  try {
    const response = await http.get('/activation/list')
    activationCodes.value = response.data.codes
  } catch (err) {
    toast.error('获取激活码列表失败')
  }
}

// 删除激活码
const deleteCode = async (codeId) => {
  const confirmed = await confirm.showConfirm(
    '删除激活码',
    '确定要删除这个激活码吗？此操作不可恢复。'
  )
  
  if (confirmed) {
    try {
      await http.delete(`/activation/${codeId}`)
      toast.success('删除成功')
      await fetchActivationCodes()
    } catch (err) {
      toast.error(err.response?.data?.error || '删除失败')
    }
  }
}

onMounted(async () => {
  await fetchStats()
  await fetchUsers()
  await fetchEssays()
  await fetchActivationCodes()
})
</script> 