from uuid import UUID

from alembic.util import status
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Task, TaskStatus, EpicStatus, Epic
from app.schemas.epics import EpicUpdate
from app.services.crud import update_item


async def epic_done_check(task_id: UUID, db: AsyncSession) -> bool:
    """
    Check if all tasks in the epic are done, except the given task_id.
    """

    # Get the epic_id from the task_id

    stmt = await db.execute(
        select(Task.epic_id).where(Task.id == task_id)
    )
    epic_id = stmt.scalar_one_or_none()

    if not task_id or not epic_id:
        return False

    result = await db.execute(
        select(Task.id).where(
            and_(
                Task.epic_id == epic_id,
                Task.id != task_id,
                Task.status != TaskStatus.DONE
            )
        )
    )
    incomplete_tasks = result.scalars().all()
    return len(incomplete_tasks) == 0


async def flip_epic_status(epic_id: UUID, db: AsyncSession):
    """
    Flip the status of the epic based on the tasks' statuses.
    If all tasks are done, set epic status to DONE, otherwise set to IN_PROGRESS.
    """
    await update_item(
        epic_id,
        EpicUpdate(status=EpicStatus.DONE),
        Epic,
        db=db
    )
    return True
