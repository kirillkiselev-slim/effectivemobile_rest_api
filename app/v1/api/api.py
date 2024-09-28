from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.responses import JSONResponse

from app.core.models.models import Order, Product, OrderItem
from app.core.schemas.schema import OrderGet, ProductGet
from .endpoints import products, orders


@products.get('/', response_model=List[ProductGet], status_code=200)
async def get_products():
    return


@products.post('/', response_model=ProductGet, status_code=201)
async def create_products():
    ...


@products.get('/{product_id}', response_model=ProductGet, status_code=200)
async def get_product():
    ...


@products.put('/{product_id}', response_model=ProductGet, status_code=200)
async def change_product():
    ...


@products.delete('/{product_id}', status_code=204)
async def delete_product():
    ...


@orders.get('/', response_model=List[OrderGet], status_code=200)
async def get_orders():
    ...


@orders.post('/order_id}', response_model=OrderGet, status_code=201)
async def create_order():
    ...


@orders.patch('/{order_id}', response_model=OrderGet, status_code=200)
async def change_order():
    ...


@orders.delete('/{order_id}', status_code=204)
async def delete_order():
    ...
