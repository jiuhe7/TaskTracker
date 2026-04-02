import asyncio
from app.database import AsyncSessionLocal, engine, Base
from app.models import User, Task
from app.core.security import get_password_hash
from sqlalchemy import select

async def test_register():
    # 先建表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("建表完成")

    async with AsyncSessionLocal() as db:
        # 检查用户名
        result = await db.execute(select(User).where(User.username == "testuser"))
        if result.scalar_one_or_none():
            print("用户名已存在，跳过插入")
            return

        # 哈希密码
        hashed = get_password_hash("testpass123")
        print("密码哈希:", hashed[:20], "...")

        # 创建用户
        new_user = User(username="testuser", email="test@example.com", hashed_password=hashed)
        db.add(new_user)
        try:
            await db.commit()
            await db.refresh(new_user)
            print("注册成功！用户ID:", new_user.id)
        except Exception as e:
            print("注册失败:", type(e).__name__, str(e))
            import traceback
            traceback.print_exc()

asyncio.run(test_register())
