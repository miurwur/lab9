from .author import Author

class App():
    def __init__(self, name: str, version: str, author: Author):
        self.__name: str = name
        self.__version: str = version
        self.__author: Author = author;

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if type(name) is str and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Ошибка при задании имени')
    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, version: float):
        if type(version) is float:
            self.__version = version;
        else:
            raise ValueError('Ошибка при задании версии')

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, author: str):
        if type(author) is str:
            self.__author = author;
        else:
            raise ValueError('Ошибка при задании автора')