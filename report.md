**Отчет по лабораторной работе №9**
Студент: Барыкина Анна
Группа: P3122

**1. Цель работы**  

Реализовать полноценные CRUD (Create, Read, Update, Delete) операции для сущностей бизнес-логики приложения отслеживания курсов валют  
Освоить работу с SQLite базой данных в памяти через модуль sqlite3  
Понять принципы первичных и внешних ключей и их роль в связях между таблицами  
Выделить контроллеры для работы с БД и для рендеринга страниц в отдельные модули  
Использовать архитектуру MVC и соблюдать разделение ответственности  
Научиться тестировать функционал на примере сущностей currency и user с использованием unittest.mock  

**2. Описание моделей, их свойств и связей**  
Модель Currency (Валюта)
```python
class Currency:
    def __init__(self, num_code: str, char_code: str, name: str, value: float, nominal: int):
        self.__num_code = num_code      # Цифровой код валюты (840)
        self.__char_code = char_code    # Символьный код (USD)
        self.__name = name              # Название валюты
        self.__value = value            # Текущий курс к рублю
        self.__nominal = nominal        # Номинал

    # Геттеры и сеттеры с валидацией
    @property
    def char_code(self):
        return self.__char_code

    @char_code.setter
    def char_code(self, val: str):
        if len(val) != 3:
            raise ValueError("Код валюты должен состоять из 3 символов")
        self.__char_code = val.upper()
```
Модель User (Пользователь)
```python
class Users_id:
    def __init__(self, name: str, age: int, email: str):
        self.__name = name    # Имя пользователя
        self.__age = age      # Возраст
        self.__email = email  # Email

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if len(name) >= 1:
            self.__name = name
        else:
            raise ValueError('Имя не может быть меньше 1 символа')
```
Модель UserCurrency (Связь пользователь-валюта)
```python
# Реализует связь "многие ко многим" между User и Currency
CREATE TABLE user_currency (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    currency_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(currency_id) REFERENCES currency(id)
);
```
Связи между моделями:

Один пользователь может быть подписан на множество валют

Одна валюта может быть в подписках у множества пользователей

Связь осуществляется через промежуточную таблицу user_currency

