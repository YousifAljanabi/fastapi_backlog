from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Epic, EpicStatus


async def get_epic_owner_and_status(
    epic_id: UUID,
    db: AsyncSession
) -> [str, EpicStatus]:
    """
    Retrieve the owner email and status of an epic by its ID.
    """
    stmt = select(Epic.owner_email, Epic.status).where(Epic.id == epic_id)
    result = await db.execute(stmt)
    epic_data = result.one_or_none()

    if not epic_data:
        raise HTTPException(
            status_code=404,
            detail=f"Epic not found."
        )

    owner_email, status = epic_data
    return owner_email, status
