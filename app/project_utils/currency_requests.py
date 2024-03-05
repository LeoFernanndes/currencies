import requests


def get_updated_currency(target_currency, start_date, end_date):
    url = f'https://fxds-public-exchange-rates-api.oanda.com/cc-api/currencies?base={target_currency}&quote=USD&data_type=general_currency_pair&start_date={start_date}&end_date={end_date}'
    response = requests.get(url)
    if response.status_code == 200:
        return float(response.json()['response'][0]['average_bid'])
    return
