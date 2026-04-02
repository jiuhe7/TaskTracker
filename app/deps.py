from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError, jwt
from app.database import AsyncSessionLocal
from app.models import User
from app.core.config import settings  # 👈 引入配置中心


async def get_db():
    """
    获取数据库会话
    这是一个依赖项函数，用于在请求处理过程中提供数据库会话对象
    使用 async with 确保会话在使用后正确关闭，避免资源泄漏
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session  # 提供数据库会话对象给依赖项
            await session.commit()
        except Exception:
            await session.rollback()  # 出现异常时回滚事务
            raise  # 重新抛出异常以便上层处理
        finally:
            await session.close()  # 确保会话被关闭


# 告诉 FastAPI 我们的 Token 是从哪里来的 (通常是 header 中的 Authorization: Bearer <token>)
# tokenUrl 告诉 Swagger UI 去哪里申请获取 Token，方便你在网页上直接测试
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")


async def get_current_user(
        token: str = Depends(OAuth2PasswordBearer(tokenUrl="token")),
        db: AsyncSession = Depends(get_db)) -> User:
    """
    获取当前用户
    这是一个依赖项函数，用于在请求处理过程中获取当前认证的用户信息
    从请求中提取JWT令牌，验证令牌的有效性，并从数据库中查询对应的用户信息
    如果令牌无效或用户不存在，抛出HTTP 401未授权异常
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user