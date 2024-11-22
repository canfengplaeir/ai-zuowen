import { reactive } from 'vue'

export const authStore = reactive({
  token: localStorage.getItem('token'),
  userId: localStorage.getItem('userId'),
  
  setAuth(token, userId) {
    this.token = token
    this.userId = userId
    localStorage.setItem('token', token)
    localStorage.setItem('userId', userId)
  },
  
  clearAuth() {
    this.token = null
    this.userId = null
    localStorage.removeItem('token')
    localStorage.removeItem('userId')
  },
  
  isAuthenticated() {
    return !!this.token
  }
}) 