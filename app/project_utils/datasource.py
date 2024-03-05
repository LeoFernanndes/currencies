from database import SessionLocal
from models.currency_value import CurrencyEnum
from repositories.currency_value import CurrencyValueRepository
from datetime import datetime


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_latest_rates_dict():
    updated_currency_values_dict = {}
    db = SessionLocal()
    repository = CurrencyValueRepository(db)
    for currency in CurrencyEnum:
        if currency.value == 'USD':
            currency_dict = {
                'value': 1,
                'date': datetime.now().__str__().split('.')[0]
            }
            updated_currency_values_dict[currency.value] = currency_dict
            continue
        most_recent_currency = repository.get_most_recent_currency(currency.value)
        if most_recent_currency:
            currency_dict = {
                'value': most_recent_currency.value,
                'date': most_recent_currency.created.__str__().split('.')[0]
            }
        else:
            currency_dict = {
                'value': 0,
                'date': datetime.now()
            }
        updated_currency_values_dict[currency.value] = currency_dict

    db.close()
    return updated_currency_values_dict
