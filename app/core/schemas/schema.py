import datetime

from pydantic import BaseModel, fields, field_validator

from api.constants import ALLOWED_STATUSES


class BaseConfigModel(BaseModel):

    class Config:
        orm_mode = True


class ProductBase(BaseConfigModel):
    name: str = fields.Field(max_length=255, min_length=3)
    description: str | None = None
    price: int = fields.Field(ge=1)
    amount_left: int = fields.Field(ge=0)


class ProductGet(ProductBase):
    id: int = fields.Field()


class ProductCreate(ProductBase):
    pass


class OrderBase(BaseConfigModel):
    created_at: datetime.datetime = datetime.datetime.now(datetime.UTC)
    status: str = fields.Field(
        min_length=5, examples=[ALLOWED_STATUSES])


class OrderGet(OrderBase):
    id: int


class OrderCreate(OrderBase):

    @field_validator('status')
    @classmethod
    def check_status(cls, status: str) -> str:
        status_lower = status.lower()
        if status_lower not in ALLOWED_STATUSES:
            raise ValueError(f'{status} not in allowed statuses')
        return status_lower

