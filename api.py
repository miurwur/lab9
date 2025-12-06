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
            User(1, "Александр Иванов"),
            User(2, "Мария Петрова"),
            User(3, "Дмитрий Сидоров"),
            User(4, "Екатерина Смирнова"),
            User(5, "Михаил Кузнецов"),
            User(6, "Анна Попова"),
            User(7, "Сергей Васильев"),
            User(8, "Ольга Новикова"),
            User(9, "Андрей Морозов"),
            User(10, "Наталья Воробьева"),
            User(11, "Игорь Соловьев"),
        ]

    def get_user_currencies(self) -> list[UserCurrency]:
        return [
            UserCurrency("R01010", 1),  # Австралийский доллар - Александр
            UserCurrency("R01060", 11),  # Армянский драм - Игорь
            UserCurrency("R01020A", 2),  # Азербайджанский манат - Мария
            UserCurrency("R01030", 5),  # Фунт стерлингов - Михаил
            UserCurrency("R01035", 7),  # Евро - Сергей
            UserCurrency("R01080", 3),  # Белорусский рубль - Дмитрий
            UserCurrency("R01090B", 6),  # Болгарский лев - Анна
            UserCurrency("R01100", 8),  # Бразильский реал - Ольга
            UserCurrency("R01105", 4),  # Венгерский форинт - Екатерина
            UserCurrency("R01115", 9),  # Гонконгский доллар - Андрей
            UserCurrency("R01135", 1),  # Датская крона - Александр
            UserCurrency("R01150", 10),  # Индийская рупия - Наталья
            UserCurrency("R01200", 2),  # Исландская крона - Мария
            UserCurrency("R01210", 3),  # Казахстанский тенге - Дмитрий
            UserCurrency("R01215", 5),  # Канадский доллар - Михаил
            UserCurrency("R01230", 7),  # Китайский юань - Сергей
            UserCurrency("R01235", 6),  # Молдавский лей - Анна
            UserCurrency("R01239", 8),  # Норвежская крона - Ольга
            UserCurrency("R01240", 4),  # Польский злотый - Екатерина
            UserCurrency("R01270", 9),  # Сингапурский доллар - Андрей
            UserCurrency("R01280", 10),  # Таджикский сомони - Наталья
            UserCurrency("R01300", 11),  # Турецкая лира - Игорь
            UserCurrency("R01335", 1),  # Украинская гривна - Александр
            UserCurrency("R01350", 2),  # Чешская крона - Мария
            UserCurrency("R01355", 3),  # Шведская крона - Дмитрий
            UserCurrency("R01370", 5),  # Швейцарский франк - Михаил
            UserCurrency("R01375", 7),  # Японская иена - Сергей
            UserCurrency("R01395", 6),  # Американский доллар - Анна
            UserCurrency("R01500", 8),  # СДР - Ольга
            UserCurrency("R01503", 4),  # Южноафриканский рэнд - Екатерина
            UserCurrency("R01520", 9),  # Вон Республики Корея - Андрей
            UserCurrency("R01530", 10),  # Новый израильский шекель - Наталья
            UserCurrency("R01535", 11),  # Киргизский сом - Игорь
            UserCurrency("R01540", 1),  # Литовский лит - Александр
            UserCurrency("R01565", 2),  # Латышский лат - Мария
            UserCurrency("R01580", 3),  # Эстонская крона - Дмитрий
            UserCurrency("R01585F", 5),  # Грузинский лари - Михаил
            UserCurrency("R01589", 7),  # ОАЭ дирхам - Сергей
            UserCurrency("R01625", 6),  # Румынский лей - Анна
            UserCurrency("R01670", 8),  # Турецкая лира (новая) - Ольга
            UserCurrency("R01675", 4),  # Аргентинское песо - Екатерина
            UserCurrency("R01685", 9),  # Чилийское песо - Андрей
            UserCurrency("R01700J", 10),  # Мексиканское песо - Наталья
            UserCurrency("R01710A", 11),  # Саудовский риял - Игорь
            UserCurrency("R01717", 1),  # Индонезийская рупия - Александр
            UserCurrency("R01720", 2),  # Таиландский бат - Мария
            UserCurrency("R01760", 3),  # Филиппинское песо - Дмитрий
            UserCurrency("R01770", 5),  # Египетский фунт - Михаил
            UserCurrency("R01775", 7),  # Вьетнамский донг - Сергей
            UserCurrency("R01800", 6),  # Кувейтский динар - Анна
            UserCurrency("R01805F", 8),  # Бахрейнский динар - Ольга
            UserCurrency("R01810", 4),  # Катарский риал - Екатерина
            UserCurrency("R01815", 9),  # Колумбийское песо - Андрей
            UserCurrency("R01820", 10),  # Перуанский соль - Наталья
            UserCurrency("R02005", 11)  # Уругвайское песо - Игорь
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