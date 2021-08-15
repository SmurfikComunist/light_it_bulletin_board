from pydantic import BaseModel, Field


class CommentBase(BaseModel):
    author: str = Field(..., min_length=1, max_length=100)
    text: str = Field(..., min_length=1, max_length=200)


class CommentCreate(CommentBase):
    post_id: int


class Comment(CommentBase):
    id: int
    post_id: int

    class Config:
        orm_mode = True
