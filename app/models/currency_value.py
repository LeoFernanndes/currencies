import enum

from sqlalchemy import Column, Integer, DateTime, Float, Enum
from database import Base


class CurrencyEnum(enum.Enum):
    USD = 'USD'
    EUR = 'EUR'
    BRL = 'BRL'
    BTC = 'BTC'
    ETH = 'ETH'


class CurrencyValue(Base):
    __tablename__ = 'currency_value'

    id = Column(Integer, primary_key=True)
    currency = Column(Enum(CurrencyEnum), index=True)
    value = Column(Float)
    created = Column(DateTime)
