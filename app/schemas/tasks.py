from uuid import UUID

from pydantic import BaseModel

from app.db.models import TaskStatus


class TaskRead(BaseModel):
    id: UUID
    title: str
    hours_estimate: int
    hours_spent: int
    status: TaskStatus

    class Config:
        orm_mode = True


class TaskCreate(BaseModel):
    title: str
    epic_id: UUID
    hours_estimate: int
    hours_spent: int = 0
    status: TaskStatus = TaskStatus.TODO

    class Config:
        orm_mode = True


class TaskUpdate(BaseModel):
    title: str | None = None
    epic_id: UUID | None = None
    hours_estimate: int | None = None
    hours_spent: int | None = None
    status: TaskStatus | None = None

    class Config:
        orm_mode = True