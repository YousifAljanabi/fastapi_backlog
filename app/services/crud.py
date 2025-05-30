from fastapi import HTTPException
from typing import TypeVar, Type, List, Optional
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

ModelType = TypeVar("ModelType", bound=DeclarativeBase)
SchemaType = TypeVar("SchemaType", bound=BaseModel)

async def get_items(
        model: Type[ModelType],
        db: AsyncSession,
        read_schema: Type[SchemaType]
) -> List[SchemaType]:
    """
    Generic function to retrieve items from the database.
    """
    stmt = select(model)
    result = await db.execute(stmt)
    items = result.scalars().all()
    return [read_schema.from_orm(item) for item in items]



async def create_item(
        item_data: SchemaType,
        model: Type[ModelType],
        db: AsyncSession,
        read_schema: Type[SchemaType]
) -> SchemaType:
    """
    Generic function to create an item in the database.
    """
    new_item = model(**item_data.dict())
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return read_schema.from_orm(new_item)


async def update_item(
        item_id: UUID,
        item_data: SchemaType,
        model: Type[ModelType],
        db: AsyncSession,
        read_schema: Optional[Type[SchemaType]] = None
) -> SchemaType:
    """
    Generic function to update an item in the database.
    """
    stmt = select(model).where(model.id == item_id)
    result = await db.execute(stmt)
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    for field, value in item_data.dict(exclude_unset=True).items():
        setattr(item, field, value)

    await db.commit()
    await db.refresh(item)
    return read_schema.from_orm(item) if read_schema else None