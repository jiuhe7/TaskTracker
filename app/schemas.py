from pydantic import BaseModel, Field,EmailStr
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    """
    任务基础模型
    定义任务的基本属性，作为其他任务相关模型的基类
    """
    title: str = Field(...,min_length=1, max_length=100, description="任务标题，必填，最大长度100字符")
    description: Optional[str] = Field(None, max_length=255, description="任务描述，可选，最大长度255字符")
    is_completed: bool = Field(False, description="任务完成状态，默认为False")

class TaskCreate(TaskBase):
    """
    创建任务模型
    用于创建新任务时的数据验证，继承自 TaskBase
    """
    pass # 创建任务只需要 title, description, is_completed，所以直接继承基类即可

class TaskUpdate(BaseModel):
    # 更新时所有字段都是可选的 (Optional)
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="任务标题，最大长度100字符")
    description: Optional[str] = Field(None, max_length=255, description="任务描述，最大长度255字符")
    is_completed: Optional[bool] = None

class TaskResponse(TaskBase):
    """
    任务响应模型
    用于返回任务数据时的格式定义，包含任务的所有属性
    """
    id: int
    created_at: datetime

    model_config = {"from_attributes": True} # 允许从ORM模型创建Pydantic模型实例

class UserBase(BaseModel):
    """
    用户基础模型
    定义用户的基本属性，作为其他用户相关模型的基类
    """
    username: str = Field(..., min_length=1, max_length=50, description="用户名，必填，最大长度50字符")
    email: EmailStr = Field(..., max_length=100, description="邮箱地址，必填，必须是有效的邮箱格式，最大长度100字符")

class UserCreate(UserBase):
    """
    创建用户模型
    用于创建新用户时的数据验证，继承自 UserBase
    """
    password: str = Field(..., min_length=6, max_length=255, description="密码，必填，最小长度6字符，最大长度255字符")

class UserResponse(UserBase):
    """
    用户响应模型
    用于返回用户数据时的格式定义，包含用户的所有属性
    """
    id: int
    model_config = {"from_attributes": True} # 允许从ORM模型创建Pydantic模型实例