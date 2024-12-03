import axios from 'axios'
import { authStore } from '../stores/auth'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '//121.199.22.180:5000/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// 请求拦截器
http.interceptors.request.use(config => {
  if (config.data instanceof FormData) {
    delete config.headers['Content-Type']
  }
  
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`
  }

  return config
}, error => {
  return Promise.reject(error)
})

// 响应拦截器
http.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      authStore.clearAuth()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default http 