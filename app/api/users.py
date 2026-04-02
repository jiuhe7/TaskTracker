from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import User
from app.schemas import UserCreate, UserResponse
from app.deps import get_db
from app.core.security import get_password_hash, verify_password, create_access_token

# 创建路由器实例，设置统一的路径前缀和 Swagger UI 标签
router = APIRouter(
    prefix="/api/users",
    tags=["用户模块 (Users)"]
)

# ==========================================
# 1. 用户注册接口
# ==========================================
@router.post("/register", response_model=UserResponse)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    注册新用户
    """
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.debug(f"注册用户: {user_in.username}, {user_in.email}")
    
    # 1. 检查用户名是否已被注册
    result_by_username = await db.execute(select(User).where(User.username == user_in.username))
    if result_by_username.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="该用户名已被注册")

    # 2. 检查邮箱是否已被注册
    result_by_email = await db.execute(select(User).where(User.email == user_in.email))
    if result_by_email.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="该邮箱已被注册")

    # 3. 将明文密码转换为哈希密码
    hashed_pwd = get_password_hash(user_in.password)
    logger.debug(f"密码哈希完成")

    # 4. 创建数据库模型实例 (注意：不保存明文密码！)
    new_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_pwd
    )

    # 5. 存入数据库
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
        logger.debug(f"用户插入成功，ID: {new_user.id}")
    except Exception as e:
        logger.error(f"数据库错误: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"数据库错误: {str(e)}")

    # 返回的数据会自动经过 UserResponse 过滤，密码绝不会被返回给前端
    return new_user


# ==========================================
# 2. 用户登录接口 (获取 Token)
# ==========================================
@router.post("/login")
async def login(
    # 注意：标准 OAuth2 登录规范要求前端使用 Form 表单 (x-www-form-urlencoded) 提交账号密码
    # OAuth2PasswordRequestForm 会自动帮我们解析表单里的 username 和 password
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    用户登录并获取 JWT 令牌
    """
    # 1. 根据用户名查询用户
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()

    # 2. 验证用户是否存在，以及密码是否正确
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. 验证通过，签发 JWT Token
    # 我们把用户的 id 存进 token 的 "sub" (subject) 字段中
    access_token = create_access_token(data={"sub": str(user.id)})

    # 4. 返回标准的 OAuth2 Token 响应格式
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }