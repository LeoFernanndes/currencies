from pydantic import BaseModel
from models.currency_value import CurrencyEnum


class CurrencyValueBase(BaseModel):
    currency: CurrencyEnum
    value: float

    class Config:
        orm_mode = True


class CurrencyValueCreate(CurrencyValueBase):
    pass


class CurrencyValue(CurrencyValueBase):
    id: int
    created: str
