from models.currency import Currency


class CurrencyController:
    """Контроллер бизнес-логики для работы с валютами"""

    def __init__(self, db_controller):
        """
        Args:
            db_controller: Объект DatabaseController для работы с БД
        """
        self.db = db_controller

    def list_currencies(self):
        """Получить все валюты (Read)"""
        return self.db.read_currencies()

    def get_currency(self, currency_id: int):
        """Получить валюту по ID (Read)"""
        return self.db.read_currency(currency_id)

    def create_currency(self, currency_data: dict):
        """
        Создать новую валюту (Create)

        Args:
            currency_data (dict): Данные валюты

        Returns:
            int: ID созданной валюты
        """
        # Валидация данных перед сохранением
        try:
            # Создаем объект Currency для валидации
            currency = Currency(
                num_code=currency_data['num_code'],
                char_code=currency_data['char_code'],
                name=currency_data['name'],
                value=currency_data['value'],
                nominal=currency_data['nominal']
            )

            # Преобразуем в словарь для БД
            data_to_save = {
                'num_code': currency.num_code,
                'char_code': currency.char_code,
                'name': currency.name,
                'value': currency.value,
                'nominal': currency.nominal
            }

            # Сохраняем в БД
            return self.db.create_currency(data_to_save)

        except (KeyError, ValueError) as e:
            raise ValueError(f"Ошибка валидации данных валюты: {e}")

    def update_currency_value(self, currency_id: int, value: float):
        """
        Обновить курс валюты (Update)

        Args:
            currency_id (int): ID валюты
            value (float): Новое значение курса

        Returns:
            bool: True если обновление успешно
        """
        if value < 0:
            raise ValueError("Курс валюты не может быть отрицательным")

        return self.db.update_currency(currency_id, value)

    def delete_currency(self, currency_id: int):
        """
        Удалить валюту (Delete)

        Args:
            currency_id (int): ID валюты

        Returns:
            bool: True если удаление успешно
        """
        return self.db.delete_currency(currency_id)

    def get_currency_by_char_code(self, char_code: str):
        """Получить валюту по символьному коду"""
        currencies = self.db.read_currencies()
        for currency in currencies:
            if currency['char_code'].upper() == char_code.upper():
                return currency
        return None
