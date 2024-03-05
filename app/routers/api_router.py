from fastapi import Query, HTTPException, APIRouter, Depends
from typing import Any
from project_utils.validators import Validator
from project_utils.converter import Converter
from database import SessionLocal
from sqlalchemy.orm import Session
from repositories.currency_value import CurrencyValueRepository
from dto.currency_value import CurrencyValueCreate
from project_utils.datasource import get_latest_rates_dict
from project_utils.datasource import get_db


router = APIRouter(prefix='/api')


@router.get('/convert')
async def convert(from_: Any = Query(alias='from', default=None), to: Any = None, amount: Any = None):
    currencies = get_latest_rates_dict()
    validation_errors = {}
    if from_ not in currencies.keys():
        validation_errors['from'] = f'Query parameter value must be one from {set(currencies.keys())}'
    if to not in currencies.keys():
        validation_errors['to'] = f'Query parameter value must be one from {set(currencies.keys())}'
    if not Validator.parse_amount(amount):
        validation_errors['amount'] = 'Query parameter value must be a positive centesimal'
    if validation_errors:
        raise HTTPException(detail=validation_errors, status_code=400)

    else:
        return {
            'from': from_,
            'to': to,
            'initial_amount': amount,
            'converted': round(Converter.run_conversion(from_, to, float(amount)), 2)
        }


@router.post('/update', status_code=201)
async def update(currency: CurrencyValueCreate, db: Session = Depends(get_db)):
    currencies = get_latest_rates_dict()
    validation_errors = {}
    if currency.currency.value not in currencies.keys():
        validation_errors['currency'] = ["USD is the index currency and it's value is fixed in 1.00"]
    if currency.currency.value.upper() == 'USD':
        validation_errors['currency'] = ["USD is the index currency and it's value is fixed in 1.00"]

    if validation_errors:
        raise HTTPException(detail=validation_errors, status_code=400)

    saved_currency = CurrencyValueRepository(db).save_currency_value(currency)
    return {'deatil': saved_currency}
