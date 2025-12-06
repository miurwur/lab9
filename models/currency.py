class Currency:
    def __init__(self, id: str, num_code: str, char_code: str, nominal: str, name: str, value: str, rate: str):
        self.__id: str = id
        self.__num_code: str = num_code
        self.__char_code: str = char_code
        self.__name: str = name
        self.__value: float = self._parse_value(value)  # Преобразуем строку в float
        self.__nominal: int = int(nominal)  # Номинал тоже может быть строкой
        self.__rate: float = self._parse_value(rate)

    def _parse_value(self, value_str: str) -> float:
        """Преобразует строку '48,6178' в float 48.6178"""
        try:
            return float(value_str.replace(',', '.'))
        except (ValueError, AttributeError):
            raise ValueError(f'Невозможно преобразовать {value_str} в число')

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, id: str) -> None:
        if isinstance(id, str):
            self.__id = id
        else:
            raise ValueError('ID валюты должен быть int')

    @property
    def num_code(self) -> str:
        return self.__num_code

    @num_code.setter
    def num_code(self, num_code: str) -> None:
        if isinstance(num_code, str) and num_code.isdigit():
            self.__num_code = num_code
        else:
            raise ValueError('Цифровой код должен быть строкой из цифр')

    @property
    def char_code(self) -> str:
        return self.__char_code

    @char_code.setter
    def char_code(self, char_code: str) -> None:
        if isinstance(char_code, str) and len(char_code) == 3:
            self.__char_code = char_code
        else:
            raise ValueError('код должен быть строкой из 3 символов')

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        if isinstance(name, str) and len(name) > 0:
            self.__name = name
        else:
            raise ValueError('Название валюты должно быть непустой строкой')

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        if isinstance(value, str):
            self.__value = self._parse_value(value)
        else:
            raise ValueError('Значение курса должно быть строкой')

    @property
    def nominal(self) -> int:
        return self.__nominal

    @nominal.setter
    def nominal(self, nominal: str) -> None:
        if isinstance(nominal, str) and nominal.isdigit():
            self.__nominal = int(nominal)
        else:
            raise ValueError('Номинал должен быть строкой с числом')

    @property
    def rate(self) -> float:
        return self.__rate

    @rate.setter
    def rate(self, rate: str) -> None:
        if isinstance(rate, str):
            self.__rate = self._parse_value(rate)
        else:
            raise ValueError('rate должно быть строкой')

    def __repr__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join(v.__repr__() for _,v in vars(self).items())
        )