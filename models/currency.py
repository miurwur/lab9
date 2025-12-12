import requests
import sys

# Класс Currency (требуется в условии 9-й ЛР)
class Currency:
    def __init__(self, num_code: str, char_code: str, name: str, value: float, nominal: int):
        self.__num_code = num_code
        self.__char_code = char_code
        self.__name = name
        self.__value = value
        self.__nominal = nominal

    @property
    def num_code(self):
        return self.__num_code

    @property
    def char_code(self):
        return self.__char_code

    @char_code.setter
    def char_code(self, val: str):
        if len(val) != 3:
            raise ValueError("Код валюты должен состоять из 3 символов")
        self.__char_code = val.upper()

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val: float):
        if val < 0:
            raise ValueError("Курс валюты не может быть отрицательным")
        self.__value = val

    @property
    def nominal(self):
        return self.__nominal


class CurrencyID():
    def __init__(self, id: str):
        # конструктор
        self.__id = id

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: str):
        if len(id) >= 1:
            self.__id = id.upper()
        else:
            raise ValueError('длина валюты не может быть меньше 1 символа')


def get_currencies(currency_codes: list, url: str = "https://www.cbr-xml-daily.ru/daily_json.js", handle=sys.stdout) -> dict:
    """
    Получает курсы валют с API Центробанка России.

    Args:
        currency_codes (list): Список символьных кодов валют (например, ['USD', 'EUR'])
        url (str): URL API Центробанка России
        handle: Поток для вывода ошибок (по умолчанию sys.stdout)

    Returns:
        dict: Словарь, где ключи - символьные коды валют, а значения - словари с данными:
              {'value': курс, 'name': название, 'nominal': номинал}
              или строки с сообщением об ошибке если валюта не найдена

    Raises:
        requests.exceptions.RequestException: При ошибках HTTP-запроса
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        currencies = {}

        if "Valute" in data:
            for code in currency_codes:
                code_upper = code.upper()  # Приводим код к верхнему регистру
                if code_upper in data["Valute"]:
                    currencies[code_upper] = {
                        'value': data["Valute"][code_upper]["Value"],
                        'name': data["Valute"][code_upper]["Name"],
                        'nominal': data["Valute"][code_upper]["Nominal"]
                    }
                else:
                    currencies[code_upper] = f"Код валюты '{code}' не найден."
        return currencies

    except requests.exceptions.RequestException as e:
        handle.write(f"Ошибка при запросе к API: {e}")
        raise requests.exceptions.RequestException('Ошибка при запросе к API')
