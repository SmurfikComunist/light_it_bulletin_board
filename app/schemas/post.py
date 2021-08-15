from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
)


class PostBase(BaseModel):
    author: str = Field(..., min_length=1, max_length=100)
    title: str = Field(..., min_length=1, max_length=100)
    text: str = Field(..., min_length=1, max_length=1000)


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
