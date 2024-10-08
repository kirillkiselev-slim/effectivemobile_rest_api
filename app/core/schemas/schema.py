import datetime
from decimal import Decimal
from typing import Dict, Annotated

from pydantic import BaseModel, fields, conint, ConfigDict

from app.v1.api.constants import (REGEX, DESCRIPTION_AMOUNT_PRODUCTS,
                                  EXAMPLE_PRODUCTS, DESCRIPTION_PRODUCTS,
                                  DESCRIPTION_STATUS)


class BaseConfigModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ProductCreateUpdate(BaseConfigModel):
    name: str = fields.Field(max_length=255, min_length=3)
    description: str | None = None
    price: Annotated[Decimal, fields.Field(Decimal, gt=0, decimal_places=2)]
    amount_left: int = fields.Field(gt=0)


class ProductGet(BaseConfigModel):
    id: int
    name: str
    description: str
    price: float
    amount_left: int


class OrderCreate(BaseConfigModel):
    status: str = fields.Field(min_length=5, default='в процессе',
                               pattern=REGEX, description=DESCRIPTION_STATUS)

    products: Dict[int, Annotated[conint(ge=1), fields.Field(
        description=DESCRIPTION_AMOUNT_PRODUCTS)]] = fields.Field(
        default_factory=dict, description=DESCRIPTION_PRODUCTS,
        examples=[EXAMPLE_PRODUCTS]
    )


class OrderGet(BaseConfigModel):
    id: int
    created_at: datetime.datetime = datetime.datetime.now(datetime.UTC)
    status: str
    products: Dict[int, int] = fields.Field(
        default_factory=dict, examples=[EXAMPLE_PRODUCTS])


class OrderStatusUpdate(BaseConfigModel):
    status: str = fields.Field(min_length=5, default='в процессе',
                               pattern=REGEX, description=DESCRIPTION_STATUS)
