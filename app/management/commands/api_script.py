# This example uses Python 2.7 and the python-request library.

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from django.core.management.base import BaseCommand
from app.models import CoinData


url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
parameters = {"start": "1", "limit": "20", "convert": "USD"}
headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": "0e539491-b409-488c-9d70-072ccb3bc9e2",
}

session = Session()
session.headers.update(headers)


def get_key(data, key):
    if key in data:
        return data[key]
    else:
        return ""


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            response = session.get(url, params=parameters)
            data = response.json()
            # print(data)

            for item in data["data"]:
                coin_id = item["id"]
                coin_name = item["name"]
                price = item["quote"]["USD"]["price"]
                last_updated = item["quote"]["USD"]["last_updated"]
                #print(price)

                check_data_exists = CoinData.objects.filter(coinId=coin_id).first()
                if check_data_exists is None:
                    create_coin = CoinData.objects.create(
                        coinId=coin_id,
                        coin_name=coin_name,
                        price=price,
                        last_updated=last_updated
                        )
                    create_coin.save()

            # for item in iterator:

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
