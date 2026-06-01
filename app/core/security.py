
from datetime import datetime, timedelta, timezone
import bcrypt
from jose import jwt
from typing import Optional
from app.core.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码

    Args:
        plain_password: 明文密码
        hashed_password: 哈希后的密码

    Returns:
        bool: 密码是否匹配
    """
    # bcrypt 只使用前 72 字节，超过部分会被忽略
    # 这里我们手动截断，避免 ValueError
    password_bytes = plain_password[:72].encode('utf-8')

    try:
        hashed_password_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_password_bytes)
    except Exception:
        # 如果验证过程出错（比如哈希格式不对），返回 False
        return False


def get_password_hash(password: str) -> str:
    """
    生成密码哈希

    Args:
        password: 明文密码

    Returns:
        str: bcrypt 哈希后的密码
    """
    # bcrypt 只使用前 72 字节
    password_bytes = password[:72].encode('utf-8')
    # 生成随机盐并加密
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    # 返回字符串
    return hashed_bytes.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建访问令牌 (JWT)

    Args:
        data: 要编码到令牌中的数据
        expires_delta: 过期时间增量，None 则使用默认值

    Returns:
        str: JWT 令牌字符串
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

