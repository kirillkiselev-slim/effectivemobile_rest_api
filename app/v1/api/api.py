from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends

from app.core.models.models import Order, Product, OrderItem
from app.core.schemas.schema import (OrderGet, ProductGet,
                                     ProductCreateUpdate, OrderCreate)
from .endpoints import products, orders
from app.core.models.database import get_db
from app.core.models.utils import get_or_404, filter_name


@products.get('/', response_model=List[ProductGet], status_code=200)
async def get_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    return result.scalars().all()


@products.post('/', response_model=ProductGet, status_code=201)
async def create_product(
        product: ProductCreateUpdate, db: AsyncSession = Depends(get_db)):
    new_product = Product(**product.model_dump())
    await filter_name(db, Product, product, select)
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product


@products.get('/{product_id}', response_model=ProductGet, status_code=200)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await get_or_404(db, Product, product_id)
    return product


@products.put('/{product_id}', response_model=ProductGet, status_code=200)
async def change_product(product_id: int, new_product: ProductCreateUpdate,
                         db: AsyncSession = Depends(get_db)):
    product = await get_or_404(db, Product, product_id)
    await filter_name(db, Product, new_product, select)
    product.name = new_product.name
    product.price = new_product.price
    product.description = new_product.description
    product.amount_left = new_product.amount_left
    await db.commit()
    await db.refresh(product)
    return product


@products.delete('/{product_id}', status_code=204)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await get_or_404(db, Product, product_id)
    await db.delete(product)
    await db.commit()
    return product


@orders.get('/', response_model=List[OrderGet], status_code=200)
async def get_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order))
    return result.scalars().all()


@orders.post('/order_id}', response_model=OrderGet, status_code=201)
async def create_order():
    ...


@orders.patch('/{order_id}', response_model=OrderGet, status_code=200)
async def change_order():
    ...


@orders.delete('/{order_id}', status_code=204)
async def delete_order(product_id: int, db: AsyncSession = Depends(get_db)):
    order = await get_or_404(db, Order, product_id)
    await db.delete(order)
    await db.commit()
    return order
