class User:
    def __init__(self, name: str):
        """
        Модель пользователя

        Args:
            name (str): Имя пользователя (минимум 1 символ)
        """
        if len(name) < 1:
            raise ValueError('Имя не может быть меньше 1 символа')

        self.__id = None  # Будет установлен при сохранении в БД
        self.__name = name

    @property
    def id(self):
        """ID пользователя (устанавливается БД)"""
        return self.__id

    @id.setter
    def id(self, value: int):
        """Установить ID (только для внутреннего использования)"""
        if value is not None and value <= 0:
            raise ValueError('ID должен быть положительным числом')
        self.__id = value

    @property
    def name(self):
        """Имя пользователя"""
        return self.__name

    @name.setter
    def name(self, name: str):
        """Установить имя пользователя с валидацией"""
        if len(name) < 1:
            raise ValueError('Имя не может быть меньше 1 символа')
        self.__name = name

    def to_dict(self):
        """Преобразовать объект в словарь для БД"""
        return {
            'id': self.__id,
            'name': self.__name
        }
