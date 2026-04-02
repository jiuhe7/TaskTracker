import asyncio
from app.database import engine
from sqlalchemy import text

async def test():
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text('SELECT 1'))
            print('DB连接成功:', result.fetchone())
    except Exception as e:
        print('DB连接失败:', type(e).__name__, str(e))

asyncio.run(test())
