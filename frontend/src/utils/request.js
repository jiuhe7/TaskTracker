import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router'

// 创建 axios 实例
const request = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 5000
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    if (error.response) {
      const { status, data } = error.response
      
      // 处理 401 Unauthorized
      if (status === 401) {
        localStorage.removeItem('token')
        ElMessage.error('登录状态已失效，请重新登录')
        router.push('/login')
      } else {
        // 其他错误处理
        const message = data.detail || '请求失败'
        ElMessage.error(message)
      }
    } else {
      ElMessage.error('网络连接异常，请稍后再试')
    }
    return Promise.reject(error)
  }
)

export default request
