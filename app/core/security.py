from datetime import datetime, timedelta, timezone
import bcrypt  # 👈 抛弃 passlib，直接导入 bcrypt
from jose import jwt
from typing import Optional
from app.core.config import settings

# ==========================================
# 1. 密码哈希配置 (完全重写)
# ==========================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    # bcrypt 要求必须是 bytes 类型，所以要 encode
    password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)

def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    password_bytes = password.encode('utf-8')
    # 生成随机盐并加密
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    # 存入数据库的是字符串，所以解码回 str
    return hashed_bytes.decode('utf-8')


# ==========================================
# 2. JWT (JSON Web Token) 配置 (保持不变!)
# ==========================================


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建访问令牌
    生成一个包含用户数据的 JWT 访问令牌，设置过期时间
    使用 JOSE 库进行 JWT 的编码和签名，确保令牌的安全性和完整性
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt