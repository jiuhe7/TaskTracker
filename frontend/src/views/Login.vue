<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <span>{{ isLogin ? '用户登录' : '用户注册' }}</span>
        </div>
      </template>

      <el-form :model="form" label-width="80px" @submit.prevent="handleSubmit">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        
        <el-form-item v-if="!isLogin" label="邮箱">
          <el-input v-model="form.email" type="email" placeholder="请输入邮箱" />
        </el-form-item>

        <el-form-item label="密码">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            show-password
          />
        </el-form-item>

        <div class="form-actions">
          <el-button type="primary" native-type="submit" :loading="loading">
            {{ isLogin ? '登录' : '注册' }}
          </el-button>
          <el-button link @click="toggleMode">
            {{ isLogin ? '还没有账号？去注册' : '已有账号？去登录' }}
          </el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '../utils/request'
import qs from 'qs'

const router = useRouter()
const isLogin = ref(true)
const loading = ref(false)

const form = reactive({
  username: '',
  email: '',
  password: ''
})

const toggleMode = () => {
  isLogin.value = !isLogin.value
  form.username = ''
  form.email = ''
  form.password = ''
}

const handleSubmit = async () => {
  if (!form.username || !form.password) {
    return ElMessage.warning('请填写完整的登录信息')
  }

  loading.value = true
  try {
    if (isLogin.value) {
      // 登录：必须使用 x-www-form-urlencoded 格式
      const data = qs.stringify({
        username: form.username,
        password: form.password
      })
      const response = await request.post('/api/users/login', data, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })
      
      localStorage.setItem('token', response.access_token)
      ElMessage.success('登录成功')
      router.push('/')
    } else {
      // 注册：JSON 格式
      await request.post('/api/users/register', {
        username: form.username,
        email: form.email,
        password: form.password
      })
      ElMessage.success('注册成功，请登录')
      isLogin.value = true
    }
  } catch (error) {
    console.error('Submit error:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f7fa;
}

.login-card {
  width: 400px;
}

.card-header {
  text-align: center;
  font-size: 1.2rem;
  font-weight: bold;
}

.form-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 20px;
}

.form-actions .el-button {
  width: 100%;
  margin-left: 0;
}
</style>
