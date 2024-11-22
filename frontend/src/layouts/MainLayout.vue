<template>
  <div class="min-h-screen bg-base-200">
    <div class="flex">
      <Sidebar 
        :current-view="currentView"
        :is-admin="isAdmin"
        @change-view="changeView"
        @logout="logout"
      />
      <div class="flex-1">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authStore } from '../stores/auth'
import Sidebar from '../components/Sidebar.vue'

export default {
  name: 'MainLayout',
  components: {
    Sidebar
  },
  
  setup() {
    const router = useRouter()
    const currentView = ref(router.currentRoute.value.name)
    const isAdmin = ref(false)

    const changeView = (view) => {
      currentView.value = view
      router.push(`/app/${view}`)
    }

    const logout = () => {
      authStore.clearAuth()
      router.push('/login')
    }

    return {
      currentView,
      isAdmin,
      changeView,
      logout
    }
  }
}
</script> 