from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.users import current_active_user
from app.db import User
from app.db.models import Epic, EpicStatus
from app.db.session import get_session
from app.schemas.epics import EpicRead, EpicCreate, EpicUpdate
from app.services.crud import get_items, create_item, update_item
from app.services.get_epic_owner import get_epic_owner_and_status

router = APIRouter()


@router.get("", response_model=List[EpicRead])
async def get_epics(
        db: AsyncSession = Depends(get_session),
        user: User = Depends(current_active_user)
):
    return await get_items(Epic, db, EpicRead)

@router.post("", response_model=EpicRead)
async def create_epic(
        epic: EpicCreate,
        db: AsyncSession = Depends(get_session),
        user: User = Depends(current_active_user)
):
    return await create_item(epic, Epic, db, EpicRead)

@router.patch("/{epic_id}", response_model=EpicRead)
async def update_epic(
        epic_id: UUID,
        epic_in: EpicUpdate,
        db: AsyncSession = Depends(get_session),
        user: User = Depends(current_active_user)
):
    owner_email, status = get_epic_owner_and_status(epic_id, db)
    if status == EpicStatus.DONE and epic_in.status == EpicStatus.OPEN and owner_email != user.email:
        raise HTTPException(
            status_code=403,
            detail="You cannot reopen an epic that is not owned by you."
        )
    return await update_item(epic_id, epic_in, Epic, db, EpicRead)
