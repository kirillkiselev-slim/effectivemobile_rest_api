from fastapi import APIRouter

products = APIRouter(
    prefix='/api/v1/products',
    tags=['products'],
    responses={404: {'description': 'Not found'}},
)

orders = APIRouter(
    prefix='/api/v1/orders',
    tags=['orders'],
    responses={404: {'description': 'Not found'}},
)
