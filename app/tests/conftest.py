import asyncio
from contextlib import ExitStack

import httpx
from dotenv import load_dotenv
import pytest
from httpx import ASGITransport
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor

from app.core.models.database import get_db, Base, DatabaseSessionManager
from app.main import app as actual_app
from app.core.models.models import Product
from app.tests.v1.constants_for_pytest import (CREATE_INCORRECT_ORDER,
                                               CREATE_ORDER, CREATE_ORDER_ID,
                                               CREATE_ORDER_AMOUNT)

load_dotenv()


@pytest.fixture(autouse=True)
async def app():
    with ExitStack():
        yield actual_app


@pytest.fixture
async def async_client():
    async with (httpx.AsyncClient(
            transport=ASGITransport(
                app=actual_app), base_url='http://test') as client):
        yield client


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


warehouse_test_db = factories.postgresql_proc(
    port=None, dbname='warehouse_test_db')


@pytest.fixture(scope='session', autouse=True)
async def sessionmanager_fixture(warehouse_test_db):
    # Set up the test database connection
    pg_host = warehouse_test_db.host
    pg_port = warehouse_test_db.port
    pg_user = warehouse_test_db.user
    pg_db = warehouse_test_db.dbname
    pg_password = warehouse_test_db.password

    connection = (f'postgresql+asyncpg://{pg_user}:{pg_password}@'
                  f'{pg_host}:{pg_port}/{pg_db}')

    sessionmanager = DatabaseSessionManager(connection, engine_kwargs={})

    with DatabaseJanitor(dbname=pg_db, version=warehouse_test_db.version,
                         host=pg_host, user=pg_user, port=pg_port,
                         password=pg_password):
        yield sessionmanager
        await sessionmanager.close()


@pytest.fixture(scope='function', autouse=True)
async def create_tables(sessionmanager_fixture):
    # Ensure that the sessionmanager is properly initialized
    async with sessionmanager_fixture.connect() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


@pytest.fixture(scope='function', autouse=True)
async def session_override(app, sessionmanager_fixture):
    async def get_db_override():
        async with sessionmanager_fixture.session() as session:
            yield session

    app.dependency_overrides[get_db] = get_db_override


@pytest.fixture
async def db_session(sessionmanager_fixture):
    async with sessionmanager_fixture.session() as session:
        yield session


@pytest.fixture
async def create_insufficient_stock_product(async_client):
    products = [
        Product(id=index, name='LowStockProduct',
                description='Test Product', price=50.00, amount_left=1)
        for index in range(1, 3)
    ]
    for product in products:
        await async_client.post('/api/v1/products/', json={
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'amount_left': product.amount_left
        })

    return products


@pytest.fixture
async def create_one_product(async_client):
    product = Product(id=CREATE_ORDER_ID, name='LowStockProduct',
                      description='Test Product',
                      price=50.00, amount_left=CREATE_ORDER_AMOUNT)
    await async_client.post('/api/v1/products/', json={
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'amount_left': product.amount_left
    })
    return product


@pytest.fixture
async def post_incorrect_order(async_client):
    return async_client.post('/api/v1/orders/', json=CREATE_INCORRECT_ORDER)


@pytest.fixture
async def post_order(async_client):
    return async_client.post('/api/v1/orders/', json=CREATE_ORDER)
