<template>
  <div class="card bg-base-100 shadow-xl">
    <div class="card-body">
      <h2 class="card-title">管理员面板</h2>
      
      <!-- 统计信息 -->
      <div class="stats shadow">
        <div class="stat">
          <div class="stat-title">总用户数</div>
          <div class="stat-value">{{ stats.userCount }}</div>
        </div>
        <div class="stat">
          <div class="stat-title">总批改数</div>
          <div class="stat-value">{{ stats.essayCount }}</div>
        </div>
        <div class="stat">
          <div class="stat-title">今日批改</div>
          <div class="stat-value">{{ stats.todayCount }}</div>
        </div>
      </div>

      <!-- 用户列表 -->
      <div class="overflow-x-auto">
        <table class="table w-full">
          <thead>
            <tr>
              <th>ID</th>
              <th>用户名</th>
              <th>注册时间</th>
              <th>作文数量</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ new Date(user.created_at).toLocaleString() }}</td>
              <td>{{ user.essay_count }}</td>
              <td>
                <button 
                  class="btn btn-error btn-xs"
                  @click="deleteUser(user.id)"
                >
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import http from '../utils/axios'
import { useToast } from '../components/Toast.vue'
import { useConfirm } from './ConfirmDialog.vue'

export default {
  setup() {
    const toast = useToast()
    const confirm = useConfirm()
    const stats = reactive({
      userCount: 0,
      essayCount: 0,
      todayCount: 0
    })
    const users = ref([])

    const fetchStats = async () => {
      try {
        const response = await http.get('/admin/stats')
        stats.value = response.data
      } catch (err) {
        toast.error('获取统计信息失败')
      }
    }
    
    const fetchUsers = async () => {
      try {
        const response = await http.get('/admin/users')
        users.value = response.data
      } catch (err) {
        toast.error('获取用户列表失败')
      }
    }
    
    const deleteUser = async (userId) => {
      const confirmed = await confirm.showConfirm(
        '删除用户',
        '确定要删除该用户吗？删除后将无法恢复，且该用户的所有作文记录也将被删除。'
      )
      
      if (confirmed) {
        try {
          await http.delete(`/admin/users/${userId}`)
          await fetchUsers()
          await fetchStats()
          toast.success('用户删除成功')
        } catch (err) {
          toast.error('删除用户失败')
        }
      }
    }

    onMounted(async () => {
      await fetchStats()
      await fetchUsers()
    })

    return {
      stats,
      users,
      deleteUser
    }
  }
}
</script> 