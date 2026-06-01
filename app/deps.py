
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError, jwt
from app.database import AsyncSessionLocal
from app.models import User
from app.core.config import settings


async def get_db():
    """
    获取数据库会话
    这是一个依赖项函数，用于在请求处理过程中提供数据库会话对象
    使用 async with 确保会话在使用后正确关闭，避免资源泄漏
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# 使用 HTTPBearer 替代 OAuth2PasswordBearer
# 这样 Swagger UI 可以直接接受 Token，不需要再次登录
security = HTTPBearer(
    scheme_name="Bearer",
    description="请输入你的 JWT Token，格式: Bearer <token>",
    auto_error=False
)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)) -> User:
    """
    获取当前用户
    从请求头 Authorization: Bearer <token> 中提取 Token 并验证
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="未认证，请先登录获取 Token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not credentials:
        raise credentials_exception

    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user

