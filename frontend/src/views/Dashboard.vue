<template>
  <div class="dashboard-container">
    <el-container>
      <el-header class="dashboard-header">
        <div class="header-title">TaskTracker</div>
        <div class="header-actions">
          <el-button type="danger" plain @click="handleLogout">退出登录</el-button>
        </div>
      </el-header>

      <el-main>
        <div class="action-bar">
          <el-button type="primary" :icon="Plus" @click="openDialog()">新增任务</el-button>
        </div>

        <el-table :data="tasks" v-loading="loading" style="width: 100%" border stripe>
          <el-table-column prop="title" label="任务名称" min-width="150" />
          <el-table-column prop="description" label="任务描述" min-width="250" show-overflow-tooltip />
          <el-table-column label="状态" width="120" align="center">
            <template #default="{ row }">
              <el-switch
                v-model="row.is_completed"
                active-text="已完成"
                inactive-text="未完成"
                inline-prompt
                @change="handleStatusChange(row)"
              />
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="180">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="180" align="center">
            <template #default="{ row }">
              <el-button size="small" :icon="Edit" @click="openDialog(row)">编辑</el-button>
              <el-popconfirm
                title="确定要删除这个任务吗？"
                @confirm="handleDelete(row.id)"
                confirm-button-text="确定"
                cancel-button-text="取消"
              >
                <template #reference>
                  <el-button size="small" type="danger" :icon="Delete">删除</el-button>
                </template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>

    <!-- 新增/编辑任务对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="editingTask.id ? '编辑任务' : '新增任务'"
      width="500px"
      @closed="resetForm"
    >
      <el-form :model="taskForm" label-width="80px">
        <el-form-item label="标题" required>
          <el-input v-model="taskForm.title" placeholder="请输入任务标题" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="taskForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入任务描述"
          />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch
            v-model="taskForm.is_completed"
            active-text="已完成"
            inactive-text="未完成"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSave" :loading="saving">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus, Edit, Delete } from '@element-plus/icons-vue'
import request from '../utils/request'

const router = useRouter()
const tasks = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const saving = ref(false)
const editingTask = ref({})

const taskForm = reactive({
  title: '',
  description: '',
  is_completed: false
})

const fetchTasks = async () => {
  loading.value = true
  try {
    const response = await request.get('/api/tasks/')
    tasks.value = response
  } catch (error) {
    console.error('Fetch error:', error)
  } finally {
    loading.value = false
  }
}

const handleLogout = () => {
  localStorage.removeItem('token')
  router.push('/login')
  ElMessage.success('已退出登录')
}

const openDialog = (row = null) => {
  if (row) {
    editingTask.value = { ...row }
    taskForm.title = row.title
    taskForm.description = row.description
    taskForm.is_completed = row.is_completed
  } else {
    editingTask.value = {}
    resetForm()
  }
  dialogVisible.value = true
}

const resetForm = () => {
  taskForm.title = ''
  taskForm.description = ''
  taskForm.is_completed = false
}

const handleSave = async () => {
  if (!taskForm.title) {
    return ElMessage.warning('请输入任务标题')
  }

  saving.value = true
  try {
    if (editingTask.value.id) {
      // 更新任务
      await request.put(`/api/tasks/${editingTask.value.id}`, taskForm)
      ElMessage.success('任务更新成功')
    } else {
      // 创建任务
      await request.post('/api/tasks/', taskForm)
      ElMessage.success('任务创建成功')
    }
    dialogVisible.value = false
    fetchTasks()
  } catch (error) {
    console.error('Save error:', error)
  } finally {
    saving.value = false
  }
}

const handleDelete = async (id) => {
  try {
    await request.delete(`/api/tasks/${id}`)
    ElMessage.success('任务已删除')
    fetchTasks()
  } catch (error) {
    console.error('Delete error:', error)
  }
}

const handleStatusChange = async (row) => {
  try {
    await request.put(`/api/tasks/${row.id}`, {
      title: row.title,
      description: row.description,
      is_completed: row.is_completed
    })
    ElMessage.success(`状态已更新为: ${row.is_completed ? '已完成' : '未完成'}`)
  } catch (error) {
    // 恢复状态
    row.is_completed = !row.is_completed
    console.error('Status update error:', error)
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString()
}

onMounted(() => {
  fetchTasks()
})
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background-color: #f0f2f5;
}

.dashboard-header {
  background-color: #409eff;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.header-title {
  font-size: 1.5rem;
  font-weight: bold;
}

.action-bar {
  margin-bottom: 20px;
  display: flex;
  justify-content: flex-end;
}

.el-main {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.el-table {
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}
</style>
