class Currency:
    def __init__(self, num_code: str, char_code: str, name: str, value: float, nominal: int):
        self.__num_code = num_code
        self.__char_code = char_code
        self.__name = name
        self.__value = value
        self.__nominal = nominal

    @property
    def id(self):
        return self.__id if hasattr(self, '_Currency__id') else None

    @id.setter
    def id(self, value: int):
        self.__id = value

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