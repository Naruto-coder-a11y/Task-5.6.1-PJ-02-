import json
import requests
from config import valute


class APIException(Exception):
    pass


#Для раобты использовалось 3 API
#API центробанка и двух зарубежных сервисов
#тк для конвертации валют из евро в доллар и наоборот необходимо изменять базовое значение валюты
#В центробанке нет такого запроса, а в зарубежных сервисах только платно
class Converter:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise APIException('Вы пытаетесь конвертировать одну валюту в точно такую же')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException('Вы неверно ввели количество конвертируемой валюты')

        if quote not in valute:
            raise APIException(f'Вы неверно ввели название валюты {quote}')

        if base == 'рубль':
            query_for_rub = requests.get('https://www.cbr-xml-daily.ru/latest.js')
            query = json.loads(query_for_rub.content)['rates'][f'{valute[quote]}']

        elif base == 'евро':
            query_for_eur = requests.get('http://data.fixer.io/api/latest?access_key=4ba30fa3ff3272d2a3c8bf50d4fe3221')
            query = json.loads(query_for_eur.content)['rates'][f'{valute[quote]}']

        elif base == 'доллар':
            query_for_usd = requests.get(
                'https://openexchangerates.org/api/latest.json?app_id=89b255803c69463183bc986d8d93a453')
            query = json.loads(query_for_usd.content)['rates'][f'{valute[quote]}']

        else:
            raise APIException(f'Вы неверно ввели название валюты {base}')
        return float(amount) * float(query)