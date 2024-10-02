from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from pydantic import ValidationError

from app.core.models.models import Order, Product, OrderItem
from app.core.schemas.schema import (OrderGet, ProductGet, OrderStatusUpdate,
                                     ProductCreateUpdate, OrderCreate)
from .endpoints import products, orders
from app.core.models.database import get_db
from app.core.models.crud import (get_or_404, filter_name,
                                  check_product_amount_and_save)


@products.get('/', response_model=List[ProductGet], status_code=200)
async def get_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).order_by(Product.id))
    return result.scalars().all()


@products.post('/', response_model=ProductGet, status_code=201)
async def create_product(
        product: ProductCreateUpdate, db: AsyncSession = Depends(get_db)):
    new_product = Product(**product.model_dump())
    await filter_name(db=db, model=Product, item=product, statement=select)
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product


@products.get('/{product_id}', response_model=ProductGet, status_code=200)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    return await get_or_404(db=db, model=Product, identifier=product_id)


@products.put('/{product_id}', response_model=ProductGet, status_code=200)
async def change_product(product_id: int, new_product: ProductCreateUpdate,
                         db: AsyncSession = Depends(get_db)):
    product = await get_or_404(db=db, model=Product, identifier=product_id)
    await filter_name(db=db, model=Product, item=new_product, statement=select)
    product.name = new_product.name
    product.price = new_product.price
    product.description = new_product.description
    product.amount_left = new_product.amount_left
    await db.commit()
    await db.refresh(product)
    return product


@products.delete('/{product_id}', status_code=204)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await get_or_404(db=db, model=Product, identifier=product_id)
    await db.delete(product)
    await db.commit()


@orders.get('/', response_model=List[OrderGet], status_code=200)
async def get_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).order_by(Order.id))
    return result.scalars().all()


@orders.get('/{order_id}', response_model=OrderGet, status_code=200)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await get_or_404(
        db=db, model=Order, join_load=True, identifier=order_id)
    return order


@orders.post('/', response_model=OrderGet, status_code=201)
async def create_order(order: OrderCreate,
                       db: AsyncSession = Depends(get_db)):
    """
    Создание нового заказа. Проверяет наличие товаров на
    складе, добавляет заказ и связанные с ним товары в
    базу данных, после чего возвращает созданный заказ.
    """
    order_dict = order.model_dump()
    products_dict = order_dict.get('products')
    new_order = Order(
        created_at=order_dict.get('created_at'),
        status=order_dict.get('status'))
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)

    await check_product_amount_and_save(
        db=db, model=Product, save_model=OrderItem,
        product_dict=products_dict, order_id=new_order.id)
    await db.refresh(new_order)
    new_order_products = await get_or_404(db=db, model=Order, join_load=True,
                                          identifier=new_order.id)
    return new_order_products


@orders.patch('/{order_id}/status', response_model=OrderGet, status_code=200)
async def change_order(order_id: int, order: OrderStatusUpdate,
                       db: AsyncSession = Depends(get_db)):
    try:
        order_in_db = await get_or_404(db, Order, order_id)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    order_in_db.status = order.status
    await db.commit()
    await db.refresh(order_in_db)
    return order_in_db


@orders.delete('/{order_id}', status_code=204)
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await get_or_404(db=db, model=Order, identifier=order_id)
    await db.delete(order)
    await db.commit()
