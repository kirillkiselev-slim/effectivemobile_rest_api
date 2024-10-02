from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.v1.api.endpoints import products, orders
from app.v1.api import api
from app.core.models.database import sessionmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, title='Склад', docs_url='/api/docs',
              redoc_url='/api/redoc')

api_start = api

app.include_router(products)
app.include_router(orders)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', reload=True, port=8000)
