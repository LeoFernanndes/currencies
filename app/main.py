import uvicorn
import time
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse
from routers.api_router import router as api_router
from database import Base, engine
from project_utils.datasource import get_latest_rates_dict
from fastapi_utils.tasks import repeat_every
from datetime import datetime, timedelta
from database import SessionLocal
from models.currency_value import CurrencyEnum
from project_utils.currency_requests import get_updated_currency
from repositories.currency_value import CurrencyValueRepository
from dto.currency_value import CurrencyValueCreate


Base.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI()
app.include_router(api_router)

templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
@repeat_every(seconds=60 * 10)
def update_currencies() -> None:
    today = datetime.now().date()
    yesterday = (datetime.now() - timedelta(days=1)).date()
    db = SessionLocal()
    repository = CurrencyValueRepository(db)
    for currency in CurrencyEnum:
        if currency.value == "USD":
            continue
        most_recent_value = repository.get_most_recent_currency(currency.value)
        if not most_recent_value:
            value = get_updated_currency(currency.value, start_date=yesterday, end_date=today)
            repository.save_currency_value(CurrencyValueCreate(currency=currency.value, value=value))
        else:
            if most_recent_value.created < datetime.now() - timedelta(hours=1):
                repository.save_currency_value(CurrencyValueCreate(currency=currency.value, value=value))
    return


@app.get('/', response_class=HTMLResponse)
async def render(request: Request):
    currencies = get_latest_rates_dict()
    return templates.TemplateResponse(
        request=request, name="home.html", context={'currencies': currencies, 'currency_keys': set(currencies.keys())}
    )


@app.get('/currencies', response_class=HTMLResponse)
async def render(request: Request):
    currencies = get_latest_rates_dict()
    return templates.TemplateResponse(
        request=request, name="currencies.html", context={'currencies': currencies, 'currency_keys': set(currencies.keys())}
    )


@app.get('/update', response_class=HTMLResponse)
async def render(request: Request):
    currencies = get_latest_rates_dict()
    currencies_ = set(currencies.keys())
    parsed_currencies = [currency.upper() for currency in currencies_]
    parsed_currencies_set = set(parsed_currencies)
    parsed_currencies_set.discard('USD')

    return templates.TemplateResponse(
        request=request, name="update_currency_form.html", context={'currency_keys': parsed_currencies_set}
    )


if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
