from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Task, User
from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.deps import get_db, get_current_user

router = APIRouter(
    prefix="/api/tasks",
    tags=["任务模块 (Tasks)"]
)


# ==========================================
# 1. 创建任务 (Create)
# ==========================================
@router.post("/", response_model=TaskResponse)
async def create_task(
        task_in: TaskCreate,
        db: AsyncSession = Depends(get_db),
        # 👇 最核心的保安：必须带有合法 Token，并在后台帮你查出是哪个 User
        current_user: User = Depends(get_current_user)
):
    """
    创建新任务，自动绑定到当前登录用户
    """
    # 将前端传来的 Pydantic 模型解包为字典，并强行打上当前用户的 ID 标签
    new_task = Task(**task_in.model_dump(), owner_id=current_user.id)

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    return new_task


# ==========================================
# 2. 获取任务列表 (Read - 分页)
# ==========================================
@router.get("/", response_model=list[TaskResponse])
async def get_tasks(
        skip: int = Query(0, description="跳过的记录数"),
        limit: int = Query(10, description="返回的记录数", le=100),
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    获取当前用户的所有任务列表（支持分页）
    """
    # 核心安全逻辑：查询条件必须加上 Task.owner_id == current_user.id
    stmt = select(Task).where(Task.owner_id == current_user.id).offset(skip).limit(limit)
    result = await db.execute(stmt)

    tasks = result.scalars().all()
    return tasks


# ==========================================
# 3. 获取单个任务详情 (Read)
# ==========================================
@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
        task_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    根据 ID 获取特定任务
    """
    # 同样必须检查归属权
    stmt = select(Task).where(Task.id == task_id, Task.owner_id == current_user.id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="任务不存在或您无权访问")

    return task


# ==========================================
# 4. 更新任务 (Update)
# ==========================================
@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
        task_id: int,
        task_in: TaskUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    更新指定任务的信息
    """
    # 先查出来确认存在且有权限
    stmt = select(Task).where(Task.id == task_id, Task.owner_id == current_user.id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="任务不存在或您无权访问")

    # exclude_unset=True 极其关键！它意味着前端只传了 title，就只更新 title，不传的不管
    update_data = task_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    await db.commit()
    await db.refresh(task)
    return task


# ==========================================
# 5. 删除任务 (Delete)
# ==========================================
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    删除指定任务
    """
    stmt = select(Task).where(Task.id == task_id, Task.owner_id == current_user.id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="任务不存在或您无权访问")

    await db.delete(task)
    await db.commit()

    # HTTP 204 No Content 代表删除成功，且不需要返回任何内容
    return None