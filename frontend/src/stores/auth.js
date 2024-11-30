import { reactive } from 'vue'

export const authStore = reactive({
  token: localStorage.getItem('token'),
  userId: localStorage.getItem('userId'),
  isAdmin: localStorage.getItem('isAdmin') === 'true',
  
  setAuth(token, userId, isAdmin) {
    this.token = token
    this.userId = userId
    this.isAdmin = Boolean(isAdmin)
    localStorage.setItem('token', token)
    localStorage.setItem('userId', userId)
    localStorage.setItem('isAdmin', String(isAdmin))
  },
  
  clearAuth() {
    this.token = null
    this.userId = null
    this.isAdmin = false
    localStorage.removeItem('token')
    localStorage.removeItem('userId')
    localStorage.removeItem('isAdmin')
  },
  
  isAuthenticated() {
    return !!this.token
  }
}) 