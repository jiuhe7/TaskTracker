# 📝 TaskTracker API

基于 **FastAPI** 和 **异步 SQLAlchemy 2.0** 构建的轻量级、高性能任务管理系统后端 API。

本项目作为 FastAPI 进阶实战项目，展示了现代 Python Web 后端开发的最佳实践，包含完整的 JWT 权限认证、依赖注入、Pydantic 数据验证以及模块化的目录架构。

## ✨ 核心特性

* **🚀 极速响应**: 基于 FastAPI 构建，原生支持异步处理 (AsyncIO)。
* **🔐 安全认证**: 使用 OAuth2 密码流和 JWT (JSON Web Tokens) 实现无状态用户身份验证。
* **🛡️ 权限隔离**: 严格的数据隔离，用户只能查看、修改和删除自己创建的任务。
* **📦 现代 ORM**: 采用 SQLAlchemy 2.0 全新异步语法，配合 MySQL/SQLite 进行数据持久化。
* **📖 自动文档**: 自动生成交互式的 Swagger UI (`/docs`) 和 ReDoc (`/redoc`) API 文档。
* **🏗️ 标准架构**: 采用企业级工程目录结构，路由、模型、业务逻辑职责分离，易于扩展和维护。

## 🛠️ 技术栈

* **Web 框架**: [FastAPI](https://fastapi.tiangolo.com/)
* **ASGI 服务器**: [Uvicorn](https://www.uvicorn.org/)
* **ORM**: [SQLAlchemy 2.0 (Async)](https://docs.sqlalchemy.org/)
* **数据验证**: [Pydantic v2](https://docs.pydantic.dev/)
* **数据库驱动**: `aiomysql` (如果使用 MySQL) 或 `aiosqlite` (如果使用 SQLite)
* **密码哈希**: `passlib[bcrypt]`
* **JWT 编码**: `python-jose`

## 📂 项目结构

```text
TaskTracker/
├── app/
│   ├── api/             # API 路由分发 (Controllers)
│   │   ├── tasks.py     # 任务相关接口
│   │   └── users.py     # 用户注册/登录接口
│   ├── core/            # 核心配置与工具 (Security, Config)
│   │   └── security.py  # JWT 生成与密码哈希逻辑
│   ├── database.py      # 数据库引擎与异步 Session 配置
│   ├── deps.py          # 全局依赖注入 (获取数据库连接、获取当前用户等)
│   ├── main.py          # FastAPI 实例初始化与应用入口
│   ├── models.py        # SQLAlchemy 数据库模型 (ORM)
│   └── schemas.py       # Pydantic 数据验证模型 (DTO)
├── .env                 # 环境变量配置文件 (勿提交至 Git)
├── requirements.txt     # Python 依赖包列表
└── README.md            # 项目说明文档