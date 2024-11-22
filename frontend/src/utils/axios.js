import axios from 'axios'
import { authStore } from '../stores/auth'

// 从环境变量获取 API 地址，如果没有则使用默认值
const API_URL = import.meta.env.VITE_API_URL || '/api'

const http = axios.create({
  baseURL: API_URL
})

// 添加请求拦截器
http.interceptors.request.use(config => {
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`
  }
  return config
})

// 添加响应拦截器
http.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      authStore.clearAuth()
      window.location.reload()
    }
    return Promise.reject(error)
  }
)

export default http 