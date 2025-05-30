from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.users import current_active_user
from app.db import User
from app.db.models import Task, TaskStatus
from app.db.session import get_session
from app.schemas.tasks import TaskRead, TaskCreate, TaskUpdate
from app.services.crud import get_items, create_item, update_item
from app.services.epic_status import epic_done_check, flip_epic_status
from app.services.get_task_hours import get_task_hours

router = APIRouter()


@router.get("", response_model=List[TaskRead])
async def get_tasks(
        db: AsyncSession = Depends(get_session),
        user: User = Depends(current_active_user)
):
    items = await get_items(Task, db, TaskRead)
    return items


@router.post("", response_model=TaskRead)
async def create_task(
        task: TaskCreate,
        db: AsyncSession = Depends(get_session),
        user: User = Depends(current_active_user)
):
    return await create_item(task, Task, db, TaskRead)


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
        task_id: UUID,
        task_in: TaskUpdate,
        db: AsyncSession = Depends(get_session),
        user: User = Depends(current_active_user)
):
    hours_estimate = await get_task_hours(task_id, db)
    if task_in.hours_spent is not None and task_in.hours_spent < hours_estimate:
        raise HTTPException(
            status_code=400,
            detail="Hours spent cannot be less than the estimated hours."
        )
    all_done = False
    if task_in.status == TaskStatus.DONE:
        all_done = await epic_done_check(task_id, db)
    updated = await update_item(task_id, task_in, Task, db, TaskRead)
    if all_done:
        await flip_epic_status(task_id, db)
    return updated
