from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.db.models import EpicStatus


class EpicRead(BaseModel):
    id: UUID
    title: str
    owner_email: EmailStr
    status: EpicStatus
    class Config:
        orm_mode = True


class EpicCreate(BaseModel):
    title: str
    owner_email: EmailStr
    status: EpicStatus = EpicStatus.OPEN

    class Config:
        orm_mode = True


class EpicUpdate(BaseModel):
    title: str | None = None
    owner_email: EmailStr | None = None
    status: EpicStatus | None = None

    class Config:
        orm_mode = True