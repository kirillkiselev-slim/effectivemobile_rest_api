from fastapi import FastAPI

from app.v1.api.endpoints import products, orders
from app.v1.api import api
from app.core.models.database import Base, engine, async_session

app = FastAPI()

api_start = api
app.include_router(products)
app.include_router(orders)


async def init_db():
    """Инициализация БД, создание всех таблиц."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event('startup')
async def on_startup():
    """Запускает инициализацию БД."""
    await init_db()


# async def get_db():
#     """Получение сессии БД для каждого запроса."""
#     async with async_session() as session:
#         yield session
