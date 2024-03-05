from sqlalchemy.orm import Session
from dto.currency_value import CurrencyValueBase
from models.currency_value import CurrencyValue
from datetime import datetime
from sqlalchemy import desc


class CurrencyValueRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_most_recent_currency(self, currency: str, limit=10):
        return self.db.query(CurrencyValue).order_by(desc('created')).filter(CurrencyValue.currency == currency).first()

    def get_values_by_currency(self, currency: str, limit=10):
        return self.db.query(CurrencyValue).order_by(desc('created')).filter(CurrencyValue.currency == currency).all()

    def save_currency_value(self, currency_value: CurrencyValueBase):
        model = CurrencyValue(currency=currency_value.currency, value=currency_value.value, created=datetime.utcnow())
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model
