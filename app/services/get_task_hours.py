from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Task


async def get_task_hours(
    task_id: UUID,
    db: AsyncSession
) -> int:
    """
    Retrieve the task estimated hours by its ID.
    """
    stmt = select(Task.hours_estimate).where(Task.id == task_id)
    result = await db.execute(stmt)
    task_data = result.one_or_none()

    if not task_data:
        raise HTTPException(
            status_code=404,
            detail=f"Task not found."
        )

    return int(task_data[0]) if task_data[0] is not None else 0

