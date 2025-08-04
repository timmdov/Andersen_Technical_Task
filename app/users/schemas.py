from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: Optional[str] = Field(None, min_length=1)
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=6)
    model_config = ConfigDict(extra="forbid")

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    username: str
    model_config = ConfigDict(from_attributes=True, extra="forbid")