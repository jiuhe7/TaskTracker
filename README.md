
# TaskTracker - 任务管理系统 API

基于 FastAPI 的高性能异步任务管理系统后端 API。

---

## 目录

- [项目简介](#项目简介)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [数据库配置](#数据库配置)
- [API 接口文档](#api-接口文档)
- [核心模块详解](#核心模块详解)
- [开发指南](#开发指南)
- [常见问题](#常见问题)

---

## 项目简介

TaskTracker 是一个完整的任务管理系统后端，具有以下特性：

- 用户注册/登录（JWT 认证）
- 任务的增删改查（CRUD）
- 用户数据隔离（每个用户只能看到自己的任务）
- 自动生成交互式 API 文档
- 完全异步处理，高性能

---

## 技术栈

| 技术 | 版本/说明 | 用途 |
|------|----------|------|
| **FastAPI** | 0.109+ | Web 框架，高性能异步 |
| **Uvicorn** | ASGI 服务器 | 运行 FastAPI 应用 |
| **SQLAlchemy** | 2.0+ | ORM，异步数据库操作 |
| **Pydantic** | 2.5+ | 数据验证和序列化 |
| **aiomysql** | MySQL 异步驱动 | 连接 MySQL 数据库 |
| **bcrypt** | 密码加密 | 安全存储用户密码 |
| **python-jose** | JWT 库 | 生成和验证访问令牌 |
| **MySQL** | 8.0+ | 数据库（可选 SQLite 替代） |

---

## 项目结构

```
TaskTracker/
├── app/                          # 应用主目录
│   ├── __init__.py               # 包初始化（空文件）
│   ├── main.py                   # FastAPI 应用入口
│   │
│   ├── api/                      # API 路由层（Controllers）
│   │   ├── __init__.py
│   │   ├── users.py              # 用户相关接口
│   │   └── tasks.py              # 任务相关接口
│   │
│   ├── core/                     # 核心工具模块
│   │   ├── __init__.py
│   │   ├── config.py             # 配置管理（环境变量）
│   │   └── security.py           # 密码哈希、JWT 令牌
│   │
│   ├── database.py               # 数据库连接配置
│   ├── models.py                 # SQLAlchemy ORM 模型（数据库表结构）
│   ├── schemas.py                # Pydantic 模型（数据验证）
│   └── deps.py                   # 依赖注入（获取数据库会话、当前用户）
│
├── .env                          # 环境变量配置
├── requirements.txt              # Python 依赖包列表
├── run_server.py                 # 快速启动脚本
└── README.md                     # 项目说明文档
```

---

## 快速开始

### 1. 环境准备

确保你已经安装了：
- Python 3.11+
- MySQL 8.0+（或者使用 SQLite，见下文）

### 2. 创建虚拟环境（推荐）

```bash
# 使用 conda
conda create -n fastapi_env python=3.11
conda activate fastapi_env

# 或使用 venv
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置数据库

编辑 `.env` 文件：

```env
# JWT 签名密钥（生产环境请更换为强密钥）
SECRET_KEY=94c1c8a14b35bc451b2e67df10b985c490a0740cfb6389f41753443a7cb147db

# MySQL 数据库连接 URL
# 格式: mysql+aiomysql://用户名:密码@主机:端口/数据库名?charset=utf8mb4
DATABASE_URL=mysql+aiomysql://root:123456@127.0.0.1:3306/tasktracker?charset=utf8mb4
```

#### 创建 MySQL 数据库

在 MySQL 中执行：

```sql
CREATE DATABASE IF NOT EXISTS tasktracker CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 想使用 SQLite 替代？

修改 `.env` 文件中的 `DATABASE_URL`：

```env
# 使用 SQLite（无需安装数据库，开箱即用）
DATABASE_URL=sqlite+aiosqlite:///./tasktracker.db
```

同时需要修改 `app/database.py` 中 `connect_args`（SQLite 可能需要）。

### 5. 启动服务器

```bash
# 方式 1: 使用启动脚本
python run_server.py

# 方式 2: 直接使用 uvicorn
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 6. 访问 API 文档

- **Swagger UI (交互式文档)**: http://127.0.0.1:8000/docs
- **ReDoc (美观文档)**: http://127.0.0.1:8000/redoc

---

## 数据库配置

### MySQL 配置示例

```env
DATABASE_URL=mysql+aiomysql://root:your_password@localhost:3306/tasktracker?charset=utf8mb4
```

### SQLite 配置示例

```env
DATABASE_URL=sqlite+aiosqlite:///./tasktracker.db
```

### 数据库表结构

项目启动时会自动创建以下表：

#### users 表（用户表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键，自增 |
| username | String(50) | 用户名，唯一 |
| email | String(100) | 邮箱，唯一 |
| hashed_password | String(255) | 加密后的密码 |

#### tasks 表（任务表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键，自增 |
| title | String(100) | 任务标题 |
| description | String(255) | 任务描述（可选） |
| is_completed | Boolean | 是否已完成，默认 False |
| created_at | DateTime | 创建时间，自动设置 |
| owner_id | Integer | 外键，关联 users.id |

---

## API 接口文档

### 认证说明

除了注册和登录接口，其他接口都需要在请求头中携带 JWT Token：

```
Authorization: Bearer <your_token_here>
```

### 用户模块 (User)

#### 1. 用户注册

- **接口**: `POST /api/users/register`
- **描述**: 注册新用户
- **请求体**:
```json
{
  "username": "string (1-50字符)",
  "email": "user@example.com",
  "password": "string (至少6位)"
}
```
- **响应 (200)**:
```json
{
  "id": 1,
  "username": "string",
  "email": "user@example.com"
}
```
- **错误 (400)**: 用户名或邮箱已存在

#### 2. 用户登录

- **接口**: `POST /api/users/login`
- **描述**: 登录获取访问令牌
- **请求格式**: `application/x-www-form-urlencoded`
- **参数**:
  - `username`: 用户名
  - `password`: 密码
- **响应 (200)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```
- **错误 (401)**: 用户名或密码错误

### 任务模块 (Tasks)

#### 1. 创建任务

- **接口**: `POST /api/tasks/`
- **认证**: 需要
- **请求体**:
```json
{
  "title": "任务标题 (必填)",
  "description": "任务描述 (可选)",
  "is_completed": false
}
```
- **响应 (200)**: 返回创建的任务详情

#### 2. 获取任务列表

- **接口**: `GET /api/tasks/`
- **认证**: 需要
- **查询参数**:
  - `skip`: 跳过的记录数，默认 0
  - `limit`: 返回的最大记录数，默认 10，最大 100
- **响应 (200)**: 任务数组

#### 3. 获取单个任务

- **接口**: `GET /api/tasks/{task_id}`
- **认证**: 需要
- **路径参数**: `task_id` - 任务 ID
- **响应 (200)**: 任务详情
- **错误 (404)**: 任务不存在或无权访问

#### 4. 更新任务

- **接口**: `PUT /api/tasks/{task_id}`
- **认证**: 需要
- **请求体** (所有字段可选，只更新提供的字段):
```json
{
  "title": "新标题",
  "description": "新描述",
  "is_completed": true
}
```
- **响应 (200)**: 更新后的任务详情

#### 5. 删除任务

- **接口**: `DELETE /api/tasks/{task_id}`
- **认证**: 需要
- **响应 (204)**: 无内容（删除成功）

---

## 核心模块详解

### 1. app/main.py - 应用入口

```python
# 功能:
# - 创建 FastAPI 应用实例
# - 配置 CORS（跨域）
# - 注册路由
# - 定义生命周期事件（启动/关闭）
# - 自动创建数据库表
```

**关键概念**:
- **生命周期管理器**: `lifespan()` 函数在启动时创建数据库表，关闭时释放资源
- **CORS 中间件**: 允许前端跨域访问

### 2. app/database.py - 数据库配置

```python
# 功能:
# - 创建异步数据库引擎 (create_async_engine)
# - 创建会话工厂 (async_sessionmaker)
# - 定义 ORM 基类 (DeclarativeBase)
```

### 3. app/models.py - ORM 模型

```python
# 定义两个 SQLAlchemy 模型:
# - User: 映射到 users 表
# - Task: 映射到 tasks 表，与 User 是多对一关系
```

### 4. app/schemas.py - Pydantic 数据验证

```python
# 定义数据验证模型:
#
# Task 相关:
# - TaskBase: 基础字段（title, description, is_completed）
# - TaskCreate: 创建任务时使用（继承 TaskBase）
# - TaskUpdate: 更新任务时使用（所有字段可选）
# - TaskResponse: 响应时使用（包含 id, created_at）
#
# User 相关:
# - UserBase: 基础字段（username, email）
# - UserCreate: 创建用户时使用（增加 password）
# - UserResponse: 响应时使用（只返回 id, username, email）
```

### 5. app/core/config.py - 配置管理

```python
# 功能:
# - 从 .env 文件加载环境变量
# - 提供 Settings 类
# - 创建全局 settings 对象
```

### 6. app/core/security.py - 安全工具

```python
# 功能:
# - verify_password(): 验证密码（bcrypt）
# - get_password_hash(): 生成密码哈希
# - create_access_token(): 创建 JWT 令牌
```

### 7. app/deps.py - 依赖注入

```python
# 功能:
# - get_db(): 提供数据库会话（异步上下文管理器）
# - get_current_user(): 从 Token 获取当前用户（认证保护）
```

### 8. app/api/users.py - 用户路由

```python
# 功能:
# - POST /register: 用户注册
# - POST /login: 用户登录
```

### 9. app/api/tasks.py - 任务路由

```python
# 功能:
# - POST /: 创建任务
# - GET /: 获取任务列表
# - GET /{task_id}: 获取单个任务
# - PUT /{task_id}: 更新任务
# - DELETE /{task_id}: 删除任务
#
# 安全机制: 所有接口都通过 Depends(get_current_user) 保护
# 查询时会过滤 owner_id == current_user.id，确保数据隔离
```

---

## 开发指南

### 如何添加新的 API 接口

1. 在 `app/schemas.py` 中定义请求/响应模型
2. 在 `app/models.py` 中定义 ORM 模型（如需要新表）
3. 在 `app/api/` 下创建新路由文件或修改现有文件
4. 在 `app/main.py` 中注册新路由

### 如何添加新的配置项

1. 在 `app/core/config.py` 的 `Settings` 类中添加字段
2. 在 `.env` 文件中添加对应环境变量

### 如何更换数据库

修改 `.env` 文件中的 `DATABASE_URL`：
- PostgreSQL: `postgresql+asyncpg://...`
- SQLite: `sqlite+aiosqlite:///...`

### 调试技巧

- 使用 `print()` 或 Python `logging` 模块
- 在 `app/database.py` 中设置 `echo=True` 可以查看 SQL 语句
- 使用 http://127.0.0.1:8000/docs 交互式测试接口

---

## 常见问题

### 1. ModuleNotFoundError: No module named 'xxx'

确保已激活虚拟环境并安装了所有依赖：
```bash
pip install -r requirements.txt
```

### 2. MySQL 连接失败

检查：
- MySQL 服务是否启动
- 用户名密码是否正确
- 数据库 `tasktracker` 是否已创建
- 主机和端口是否正确

### 3. JWT Token 验证失败

- 确保 Token 格式正确: `Bearer <token>`
- 检查 Token 是否已过期（默认 30 分钟）
- 检查 `SECRET_KEY` 是否一致

### 4. 跨域 (CORS) 问题

在 `app/main.py` 中修改 `allow_origins` 配置：
```python
allow_origins=["http://localhost:5173", "http://localhost:3000"]
```

### 5. 如何修改 Token 过期时间？

在 `app/core/config.py` 中添加或修改：
```python
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 改为 60 分钟
```

在 `.env` 中也可以直接设置：
```env
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## 部署建议

生产环境中请注意：

1. **更换 SECRET_KEY**: 使用强随机密钥
2. **关闭 debug 模式**: `app = FastAPI(debug=False)`
3. **配置 CORS**: 只允许你的前端域名
4. **使用环境变量**: 不要把敏感信息提交到代码库
5. **使用数据库迁移工具**: 如 Alembic，替代 `create_all()`
6. **配置日志**: 使用专业的日志系统

---

## 许可证

MIT License

---

## 联系方式

如有问题，欢迎提出 Issue！

