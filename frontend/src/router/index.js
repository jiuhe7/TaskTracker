import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { public: true }
  },
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由全局守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  // 如果访问非公开页面且没有 token，重定向到登录页
  if (!to.meta.public && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    // 如果已登录还想去登录页，重定向到首页
    next('/')
  } else {
    next()
  }
})

export default router
