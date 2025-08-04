from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Generic, TypeVar
from enum import Enum

T = TypeVar('T')

class TaskCRUDResult(str, Enum):
    SUCCESS = "SUCCESS"
    NOT_FOUND = "NOT_FOUND"
    ACCESS_DENIED = "ACCESS_DENIED"
    VALIDATION_ERROR = "VALIDATION_ERROR"

class TaskStatus(str, Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.NEW)
    model_config = ConfigDict(extra="forbid")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus] = None
    model_config = ConfigDict(extra="forbid")

class TaskResponse(TaskBase):
    id: int = Field(...)
    user_id: int = Field(...)
    model_config = ConfigDict(from_attributes=True, extra="forbid")

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T] = Field(...)
    total: int = Field(...)
    page: int = Field(..., ge=1)
    pages: int = Field(..., ge=0)
    size: int = Field(..., ge=1)
    has_next: bool = Field(...)
    has_prev: bool = Field(...)
    model_config = ConfigDict(from_attributes=True)