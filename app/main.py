from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 导入我们的数据库配置和模型
from app.database import engine, Base
from app.models import User, Task  # 必须导入模型，这样 Base.metadata 才能发现它们

# 导入我们写好的业务路由
from app.api.users import router as users_router
from app.api.tasks import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI 生命周期管理器 (Lifespan)
    在这里定义的代码会在程序启动时运行一次，yield 之后的部分会在程序关闭时运行。
    """
    print("正在连接数据库并检查表结构...")
    # 启动时：根据 models.py 自动在数据库中创建表 (如果表已经存在则跳过)
    # 注意：在真实的生产环境中，我们通常会使用 Alembic 这种迁移工具，而不是直接 create_all
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("数据库表结构准备完毕！")

    yield  # 程序在这里一直运行，处理用户的各种请求...

    # 关闭时：释放数据库连接
    print("程序正在关闭，正在清理数据库连接...")
    await engine.dispose()


# 创建 FastAPI 实例
app = FastAPI(
    title="TaskTracker API",
    description="一个高性能的异步任务管理系统，包含完整的 JWT 安全认证。",
    version="1.0.0",
    lifespan=lifespan,  # 挂载生命周期管理器
    debug=True
)

# 配置跨域资源共享 (CORS)
# 如果你以后要用 Vue 或 React 写前端页面，前端向后端发请求时会被浏览器拦截，这个配置就是用来放行的。
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中千万别写 "*"！一定要写明确的前端域名 (比如 ["http://localhost:5173"])
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有的 HTTP 方法 (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # 允许所有的请求头
)

# 组装模块：把前台接待员 (Routers) 注册到大总管 (FastAPI) 这里
app.include_router(users_router)
app.include_router(tasks_router)


# 一个简单的测试接口，访问 127.0.0.1:8000/ 会看到这句问候
@app.get("/", tags=["根目录"])
async def root():
    return {
        "message": "欢迎来到 TaskTracker API 系统！🚀",
        "docs_url": "请访问 http://127.0.0.1:8000/docs 体验互动式 API 文档"
    }