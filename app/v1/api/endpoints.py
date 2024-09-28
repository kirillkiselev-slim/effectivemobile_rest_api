from fastapi import APIRouter

products = APIRouter(
    prefix='/products',
    tags=['products'],
    responses={404: {'description': 'Not found'}},
)

orders = APIRouter(
    prefix='/orders',
    tags=['orders'],
    responses={404: {'description': 'Not found'}},
)
