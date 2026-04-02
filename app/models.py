"""
数据库模型定义文件
使用 SQLAlchemy ORM 定义数据表结构
本文件定义了 User（用户）和 Task（任务）两个核心数据模型
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base

class User(Base):
    """
    用户模型
    对应数据库中的 users 表，存储系统用户信息
    """
    __tablename__ = "users"  # 数据库表名

    # 主键，自增整数，建立索引以提高查询效率
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # 用户名，最大长度50字符，必须唯一，建立索引
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    
    # 邮箱地址，最大长度100字符，必须唯一，建立索引
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    
    # 哈希后的密码，使用安全哈希算法处理，绝不存储明文密码
    # 长度255字符以容纳各种哈希算法的输出
    hashed_password: Mapped[str] = mapped_column(String(255))
    
    # 建立一对多关系：一个用户可以拥有多个任务
    # back_populates="owner" 创建双向关系，使 Task.owner 可以反向访问
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="owner")


class Task(Base):
    """
    任务模型
    对应数据库中的 tasks 表，存储用户创建的任务信息
    """
    __tablename__ = "tasks"  # 数据库表名

    # 主键，自增整数，建立索引以提高查询效率
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # 任务标题，最大长度100字符，建立索引以便按标题搜索
    title: Mapped[str] = mapped_column(String(100), index=True)
    
    # 任务描述，可选字段，最大长度255字符，允许为空
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    
    # 任务完成状态，布尔值，默认值为 False（未完成）
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # 任务创建时间，使用数据库服务器的当前时间作为默认值
    # func.now() 在数据库层面生成时间戳，确保时间一致性
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    # 外键：关联到 users 表的 id 字段
    # 表示这个任务属于哪个用户
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # 建立多对一关系：一个任务属于一个用户
    # back_populates="tasks" 创建双向关系，与 User.tasks 对应
    owner: Mapped["User"] = relationship("User", back_populates="tasks")
