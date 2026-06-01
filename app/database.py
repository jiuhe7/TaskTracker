from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings  # 👈 引入配置中心


engine = create_async_engine(
    settings.DATABASE_URL,  # 从配置中心获取数据库连接URL
    echo=True,  # 输出SQL语句到控制台，便于调试
    pool_size=10,  # 连接池大小，控制同时打开的数据库连接数量
    max_overflow=20  # 连接池溢出时允许的最大
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,  # 提交后不自动过期对象，保持对象状态
    class_=AsyncSession  # 使用异步会话类
)


class Base(DeclarativeBase):
    pass
