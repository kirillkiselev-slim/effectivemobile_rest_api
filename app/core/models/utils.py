from typing import Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Depends

from app.core.models.models import Base

ModelType = TypeVar('ModelType', bound=Base)


async def get_or_404(
    db: AsyncSession,
    model: Type[ModelType],
    identifier: int,
) -> ModelType:
    """
    Generic function to retrieve an object by its primary key.
    Raises a 404 error if not found.
    """
    obj = await db.get(model, identifier)

    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{model.__name__} with ID {identifier} not found.'
        )
    return obj
