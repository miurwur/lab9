# Исходный код get_currencies (без логирования).
import requests
from bs4 import BeautifulSoup
from typing import Dict, List

# from logger import logger
# import sys


default_list = ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'KZT', 'CHF', 'CAD', 'AUD',
                'SGD', 'HKD', 'NOK', 'SEK', 'TRY', 'PLN', 'DKK', 'HUF', 'CZK',
                'RON', 'BGN', 'BRL', 'INR', 'UAH', 'BYN', 'AMD']


def get_currencies(currency_codes: List[str] = default_list, url: str = "https://www.cbr.ru/scripts/XML_daily.asp") -> \
Dict[str, float]:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"API недоступен: {e}")
    try:
        soup = BeautifulSoup(response.content, 'xml')
        valute_elements = soup.find_all('Valute')
        if not valute_elements:
            raise KeyError("Ключ 'Valute' не найден в ответе API")
        all_valutes: Dict[str, float] = {}
        for valute in valute_elements:
            char_code_elem = valute.find('CharCode')
            value_elem = valute.find('Value')
            if char_code_elem is None or value_elem is None:
                continue
            char_code = char_code_elem.text
            value_text = value_elem.text
            try:
                rate_value = float(value_text.replace(',', '.'))
            except (ValueError, TypeError):
                raise TypeError(f"Курс валюты {char_code} имеет неверный тип: {value_text}")
            all_valutes[char_code] = rate_value
        result: Dict[str, float] = {}
        for code in currency_codes:
            if code not in all_valutes:
                raise KeyError(f"Валюта {code} отсутствует в данных")
            result[code] = all_valutes[code]
        return result
    except Exception as e:
        if isinstance(e, (KeyError, TypeError)):
            raise e
        raise ValueError(f"Некорректные данные в ответе API: {e}")


if __name__ == "__main__":
    try:
        rates = get_currencies()  # заданы стандартные параметры
        # print(rates) #print result

    except ConnectionError as e:
        print(f"Ошибка соединения: API недоступен {e}")
        raise
    except ValueError as e:
        print(f"Ошибка данных: Некорректный JSON {e}")
        raise
    except KeyError as e:
        print(f"Ошибка ключа: Нет ключа “Valute” или валюта отсутствует в данных{e}")
        raise
    except TypeError as e:
        print(f"Ошибка типа: Курс валюты имеет неверный тип	 {e}")
        raise