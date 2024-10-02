import pytest

from fastapi import status
from sqlalchemy import select

from .constants_for_pytest import INSUFFICIENT_STOCK_MESSAGE
from app.core.models.models import Product


pytest.mark.asyncio = pytest.mark.asyncio(loop_scope='function')


async def test_insufficient_stock_and_error(
        post_incorrect_order, create_insufficient_stock_product):
    response = await post_incorrect_order
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert INSUFFICIENT_STOCK_MESSAGE in response.json()['detail']


async def test_decrease_amount_of_product(
        post_order, create_one_product, async_client, db_session):
    response = await post_order
    assert response.status_code == status.HTTP_201_CREATED
    result = await db_session.execute(select(Product).where(Product.id == 1))
    product = result.scalar()
    assert product.amount_left == 0
