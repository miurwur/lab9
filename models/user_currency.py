class UserCurrency:
    def __init__(self, user_id: int, currency_id: int):
        """
        Модель связи пользователя и валюты (многие-ко-многим)

        Args:
            user_id (int): ID пользователя
            currency_id (int): ID валюты
        """
        if user_id <= 0:
            raise ValueError('ID пользователя должен быть положительным числом')

        if currency_id <= 0:
            raise ValueError('ID валюты должен быть положительным числом')

        self.__id = None  # Будет установлен при сохранении в БД
        self.__user_id = user_id
        self.__currency_id = currency_id

    # Геттеры и сеттеры

    @property
    def id(self):
        """ID связи (устанавливается БД)"""
        return self.__id

    @id.setter
    def id(self, value: int):
        """Установить ID связи"""
        if value is not None and value <= 0:
            raise ValueError('ID должен быть положительным числом')
        self.__id = value

    @property
    def user_id(self):
        """ID пользователя"""
        return self.__user_id

    @user_id.setter
    def user_id(self, value: int):
        """Установить ID пользователя"""
        if value <= 0:
            raise ValueError('ID пользователя должен быть положительным числом')
        self.__user_id = value

    @property
    def currency_id(self):
        """ID валюты"""
        return self.__currency_id

    @currency_id.setter
    def currency_id(self, value: int):
        """Установить ID валюты"""
        if value <= 0:
            raise ValueError('ID валюты должен быть положительным числом')
        self.__currency_id = value

    def to_dict(self):
        """Преобразовать объект в словарь для БД"""
        return {
            'id': self.__id,
            'user_id': self.__user_id,
            'currency_id': self.__currency_id
        }

    def __repr__(self):
        return f"UserCurrency(id={self.__id}, user_id={self.__user_id}, currency_id={self.__currency_id})"