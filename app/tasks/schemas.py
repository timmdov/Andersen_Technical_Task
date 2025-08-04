from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum

class TaskCRUDResult(str, Enum):
    SUCCESS = "success"
    NOT_FOUND = "not_found"
    ACCESS_DENIED = "access_denied"
    VALIDATION_ERROR = "validation_error"

class TaskStatus(str, Enum):
    NEW = "New"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    status: TaskStatus = Field(default=TaskStatus.NEW, description="Task status")
    model_config = ConfigDict(extra="forbid")


class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus] = None
    model_config = ConfigDict(extra="forbid")


class TaskResponse(TaskBase):
    id: int = Field(..., description="Task ID")
    user_id: int = Field(..., description="ID of the user who owns this task")
    model_config = ConfigDict(from_attributes=True, extra="forbid")


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int
    page: int = Field(1, ge=1)
    size: int = Field(20, ge=1)
