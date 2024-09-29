import datetime
from typing import Dict, List

from pydantic import BaseModel, fields, field_validator

from app.v1.api.constants import (ALLOWED_STATUSES,
                                  EXAMPLE_PRODUCTS, DESCRIPTION)


class BaseConfigModel(BaseModel):

    class Config:
        from_attributes = True


class ProductCreateUpdate(BaseConfigModel):
    name: str = fields.Field(max_length=255, min_length=3)
    description: str | None = None
    price: int = fields.Field(ge=1)
    amount_left: int = fields.Field(ge=0)


class ProductGet(BaseConfigModel):
    id: int
    name: str
    description: str
    price: int
    amount_left: int


class OrderCreate(BaseConfigModel):
    status: str = fields.Field(min_length=5, default='в процессе')
    products: Dict[int, int] = fields.Field(
        Dict, description=DESCRIPTION, examples=[EXAMPLE_PRODUCTS])

    @field_validator('status')
    @classmethod
    def check_status(cls, status: str) -> str:
        status_lower = status.lower()
        if status_lower not in ALLOWED_STATUSES:
            raise ValueError(f'{status} not in allowed statuses')
        return status_lower


class OrderGet(BaseConfigModel):
    id: int
    created_at: datetime.datetime = datetime.datetime.now(datetime.UTC)
    status: str
    products: List = fields.Field(default_factory=list)


class OrderUpdate(BaseConfigModel):
    status: str = fields.Field(min_length=5, default='в процессе')

    @field_validator('status')
    @classmethod
    def check_status(cls, status: str) -> str:
        status_lower = status.lower()
        if status_lower not in ALLOWED_STATUSES:
            raise ValueError(f'"{status}" недопустимый статус.'
                             f'Весь список статусов {ALLOWED_STATUSES}')
        return status_lower
