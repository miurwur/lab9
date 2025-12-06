from abc import ABC, abstractmethod
from models.currency import Currency
from models.user import User
from models.user_currency import UserCurrency
from typing import Optional
import requests
from bs4 import BeautifulSoup


class Api(ABC):
    @abstractmethod
    def get_currencies(self, currency_codes: Optional[list[str]] = None) -> list[Currency]:
        pass

    @abstractmethod
    def get_users(self) -> list[User]:
        pass

    @abstractmethod
    def get_user_currencies(self) -> list[UserCurrency]:
        pass

class MockApi(Api):
    def get_currencies(self, currency_codes: Optional[list[str]] = None) -> list[Currency]:
        return [
            Currency("1", '100', 'USD', '1', 'Доллар США', '76.9708', "0.5"),
            Currency("2", '101', 'EUR', '1', 'Евро', '89.9011', "0.5"),
            Currency("3", '102', 'GBP', '1', 'Фунт стерлингов', '102.6098', "0.5"),
            Currency("4", '103', 'JPY', '1', 'Японская иена', '49.585', "0.5"),
            Currency("5", '104', 'CNY', '1', 'Китайский юань', '10.8487', "0.5"),
            Currency("6", '105', 'KZT', '1', 'Казахстанский тенге', '15.2753', "0.5"),
            Currency("7", '106', 'CHF', '1', 'Швейцарский франк', '96.2496', "0.5"),
            Currency("8", '107', 'CAD', '1', 'Канадский доллар', '55.1802', "0.5"),
            Currency("9", '108', 'AUD', '1', 'Австралийский доллар', '50.9085', "0.5"),
            Currency("10", '109', 'SGD', '1', 'Сингапурский доллар', '59.3865', "0.5"),
            Currency("11", '110', 'HKD', '1', 'Гонконгский доллар', '99.0615', "0.5"),
            Currency("12", '111', 'NOK', '1', 'Норвежская крона', '76.3819', "0.5"),
            Currency("13", '112', 'SEK', '1', 'Шведская крона', '81.9804', "0.5"),
            Currency("14", '113', 'TRY', '1', 'Турецкая лира', '18.1499', "0.5"),
            Currency("15", '114', 'PLN', '1', 'Польский злотый', '21.2503', "0.5"),
            Currency("16", '115', 'DKK', '1', 'Датская крона', '12.0244', "0.5"),
            Currency("17", '116', 'HUF', '1', 'Венгерский форинт', '23.5522', "0.5"),
            Currency("18", '117', 'CZK', '1', 'Чешская крона', '37.256', "0.5"),
            Currency("19", '118', 'RON', '1', 'Румынский лей', '17.6373', "0.5"),
            Currency("20", '119', 'BGN', '1', 'Болгарский лев', '45.919', "0.5"),
            Currency("21", '120', 'BRL', '1', 'Бразильский реал', '14.4924', "0.5"),
            Currency("22", '121', 'INR', '1', 'Индийская рупия', '85.3463', "0.5"),
            Currency("23", '122', 'UAH', '1', 'Украинская гривна', '18.2381', "0.5"),
            Currency("24", '123', 'BYN', '1', 'Белорусский рубль', '26.5811', "0.5"),
            Currency("25", '124', 'AMD', '1', 'Армянский драм', '20.1949', "0.5")
        ]

    def get_users(self) -> list[User]:
        return [
            User(1, "Бред Питт"),
            User(2, "Самовар Самоваров"),
            User(3, "Миллионер Миллиардерович"),
            User(4, "Роза Тихонова"),
            User(5, "Петр Скалкин"),
            User(6, "Тимофей Скакалкин"),
            User(7, "Катя Адушкина"),
            User(8, "Прасковья Изподмосковья"),
            User(9, "Редиска Огородовна"),
            User(10, "Ольга Любимка"),
            User(11, "Огузок Трясогузкин"),
        ]

    def get_user_currencies(self) -> list[UserCurrency]:
        return [
            UserCurrency("R01010", 4),
            UserCurrency("R01060", 11),
            UserCurrency("R01020A", 10),
            UserCurrency("R01030", 4),
            UserCurrency("R01035", 4),
            UserCurrency("R01080", 4),
            UserCurrency("R01090B", 4),
            UserCurrency("R01100", 4),
            UserCurrency("R01105", 4),
            UserCurrency("R01115", 4),
            UserCurrency("R01135", 4),
            UserCurrency("R01150", 4),
            UserCurrency("R01200", 4),
            UserCurrency("R01210", 4),
            UserCurrency("R01215", 4),
            UserCurrency("R01230", 4),
            UserCurrency("R01235", 4),
            UserCurrency("R01239", 4),
            UserCurrency("R01240", 4),
            UserCurrency("R01270", 4),
            UserCurrency("R01280", 4),
            UserCurrency("R01300", 4),
            UserCurrency("R01335", 4),
            UserCurrency("R01350", 4),
            UserCurrency("R01355", 4),
            UserCurrency("R01370", 4),
            UserCurrency("R01375", 4),
            UserCurrency("R01395", 4),
            UserCurrency("R01500", 4),
            UserCurrency("R01503", 4),
            UserCurrency("R01520", 4),
            UserCurrency("R01530", 4),
            UserCurrency("R01535", 4),
            UserCurrency("R01540", 4),
            UserCurrency("R01565", 4),
            UserCurrency("R01580", 4),
            UserCurrency("R01585F", 4),
            UserCurrency("R01589", 4),
            UserCurrency("R01625", 4),
            UserCurrency("R01670", 4),
            UserCurrency("R01675", 4),
            UserCurrency("R01685", 4),
            UserCurrency("R01700J", 4),
            UserCurrency("R01710A", 4),
            UserCurrency("R01717", 4),
            UserCurrency("R01720", 4),
            UserCurrency("R01760", 4),
            UserCurrency("R01770", 4),
            UserCurrency("R01775", 4),
            UserCurrency("R01800", 4),
            UserCurrency("R01805F", 4),
            UserCurrency("R01810", 4),
            UserCurrency("R01815", 4),
            UserCurrency("R01820", 4),
            UserCurrency("R02005", 4)
        ]

class ApplicationApi(Api):
    CURRENCY_CODES_DEFAULT = ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'KZT', 'CHF', 'CAD', 'AUD',
                'SGD', 'HKD', 'NOK', 'SEK', 'TRY', 'PLN', 'DKK', 'HUF', 'CZK',
                'RON', 'BGN', 'BRL', 'INR', 'UAH', 'BYN', 'AMD']

    def get_currencies(self, currency_codes: Optional[list[str]] = None) -> list[Currency]:
        currency_codes = currency_codes or ApplicationApi.CURRENCY_CODES_DEFAULT

        url = "https://www.cbr.ru/scripts/XML_daily.asp"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"API недоступен: {e}")

        #parse XML
        try:
            soup = BeautifulSoup(response.content, 'xml')
            valute_elements = soup.find_all('Valute')

            if not valute_elements:
                raise KeyError("Ключ 'Valute' не найден в ответе API")

            result: list[Currency] = []

            for valute in valute_elements:
                id = valute.get('ID')
                num_code_elem = valute.find('NumCode')
                char_code_elem = valute.find('CharCode')
                nominal_elem = valute.find('Nominal')
                name_elem = valute.find('Name')
                value_elem = valute.find('Value')
                rate_elem = valute.find('VunitRate')

                if not all((num_code_elem, char_code_elem, nominal_elem, name_elem, value_elem, rate_elem)):
                    continue

                num_code = num_code_elem.text
                char_code = char_code_elem.text
                nominal = nominal_elem.text
                name = name_elem.text
                value = value_elem.text
                rate = rate_elem.text

                #check type course
                try:
                    rate_value = float(value.replace(',', '.'))
                except (ValueError, TypeError):
                    raise TypeError(f"Курс валюты {char_code} имеет неверный тип: {value}")

                result.append(Currency(
                    id,
                    num_code,
                    char_code,
                    nominal,
                    name,
                    value,
                    rate
                ))

            return result

        except Exception as e:
            if isinstance(e, (KeyError, TypeError)):
                raise e
            raise ValueError(f"Некорректные данные в ответе API: {e}")

    def get_users(self) -> list[User]:
        return MockApi().get_users()

    def get_user_currencies(self) -> list[UserCurrency]:
        return MockApi().get_user_currencies()