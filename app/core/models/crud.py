from typing import Type, TypeVar, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.core.models.models import Base
from app.v1.api.constants import PRODUCT_EXISTS


ModelType = TypeVar('ModelType', bound=Base)
ItemType = TypeVar('ItemType', bound=BaseModel)


async def get_or_404(
        db: AsyncSession,
        model: Type[ModelType],
        identifier: Optional[int] = None,
        join_load: Optional[bool] = None,
) -> ModelType:
    """
    Функция, которая возвращает объект по ИД. Если select_load=True,
    то выполняется запрос для выборки полей product_id и amount_of_product.
    """
    exception = HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'{model.__name__} с ИД {identifier} не найден.'
            )
    if not join_load and identifier:
        obj = await db.get(model, identifier)
        if not obj:
            raise exception
        return obj

    elif join_load and identifier:
        query = await db.execute(
            select(model).options(
                joinedload(model.order_items)).where(model.id == identifier)
        )
        order = query.scalars().first()

        if not order:
            raise exception
        products = {item.product_id: item.amount_of_product
                    for item in order.order_items}
        return {
            'id': order.id,
            'created_at': order.created_at,
            'status': order.status,
            'products': products
        }


async def filter_name(
        db: AsyncSession,
        model: Type[ModelType],
        item: ItemType,
        statement):
    """
    Функция, которая проверяет наличие такого же имени продукта.
    """
    result = await db.execute(
        statement(model).filter(model.name == item.name))

    product_in_db = result.scalars().first()
    if product_in_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=PRODUCT_EXISTS)


async def check_product_amount_and_save(
        db: AsyncSession,
        model: Type[ModelType],
        save_model: Type[ModelType],
        product_dict: Dict,
        order_id):
    """
    Проверяет наличие достаточного количества товара на складе и сохраняет заказ.
    Если запрашиваемое количество превышает доступное, выбрасывается ошибка.
    """
    for product_id, amount_request in product_dict.items():
        product = await get_or_404(db, model, product_id)
        if amount_request <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Для продукта {product.name} '
                                       f'нужно указать значения 1 или выше')
        if product.amount_left < amount_request:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Нет кол-во для {product.name}'
                                       f' (ID: {product_id}). '
                                       f'Доступно: {product.amount_left},'
                                       f' Запрошено: {amount_request}')
        order_item = save_model(order_id=order_id, product_id=int(product_id),
                                amount_of_product=amount_request)
        db.add(order_item)
        product.amount_left -= amount_request
        db.add(product)
    await db.commit()
