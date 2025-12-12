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

**3. Структура проекта** 
my_App/  
├── controllers/                    # Контроллеры (архитектура MVC)  
│   ├── __init__.py  
│   ├── databasecontroller.py      # Низкоуровневый контроллер БД  
│   └── currencycontroller.py      # Бизнес-логика для валют  
├── models/                        # Модели предметной области  
│   ├── __init__.py  
│   ├── currency.py  
│   ├── users.py  
│   └── currencies_users.py  
├── templates/                     # HTML шаблоны  
│   ├── currency_input.html  
│   ├── currencies_users.html  
│   ├── currency_result.html  
│   ├── user_page.html  
│   ├── page1.html  
│   └── page2.html  
├── test_currency.py               # Тесты для валют  
├── test_user_model.py             # Тесты для пользователей  
├── my_App.py                      # Главный файл приложения  
└── README.md  



**3. Описание моделей, их свойств и связей**  
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

**4. Реализация CRUD с примерами SQL-запросов**  
Create - добавление новой валюты  
```python
# Метод в databasecontroller.py
def _create(self, data):
    with closing(self.connection.cursor()) as cursor:
        cursor.execute("""
            INSERT INTO currency(num_code, char_code, name, value, nominal)
            VALUES(:num_code, :char_code, :name, :value, :nominal)
        """, data)  # Параметризованный запрос
        self.connection.commit()
        return cursor.lastrowid

# Использование:
db_crud._create({
    'num_code': '840',
    'char_code': 'USD',
    'name': 'Доллар США',
    'value': 90.0,
    'nominal': 1
})
```
Read - получение всех валют
```python
def _read(self):
    with closing(self.connection.cursor()) as cursor:
        cursor.execute("SELECT * FROM currency ORDER BY char_code")
        return [dict(row) for row in cursor.fetchall()]

# В контроллере:
def list_currencies(self):
    return self.db._read()
```
Update - изменение курса валюты
```python
def _update(self, updates):
    with closing(self.connection.cursor()) as cursor:
        for char_code, new_value in updates.items():
            cursor.execute(
                "UPDATE currency SET value = ? WHERE UPPER(char_code) = UPPER(?)",
                (new_value, char_code)  # Параметризованный запрос
            )
        self.connection.commit()
    return True

# Пример запроса: UPDATE currency SET value = 95.5 WHERE char_code = 'USD'
```
Delete - удаление валюты по ID
```python
def _delete(self, currency_id):
    with closing(self.connection.cursor()) as cursor:
        cursor.execute("DELETE FROM currency WHERE id = ?", (currency_id,))
        self.connection.commit()
        return cursor.rowcount > 0

# Пример запроса: DELETE FROM currency WHERE id = 1
```

5. Скриншоты работы приложения
5.1 Главная страница (/currency) - таблица валют с CRUD операциями:  
   <img width="1087" height="544" alt="Снимок" src="https://github.com/user-attachments/assets/32d4fca3-b608-4107-85d7-72a793ad4671" />
   Загрузка актуальных данных о валютах с ЦБ РФ:  
<img width="1025" height="523" alt="2" src="https://github.com/user-attachments/assets/c3adc07c-6d29-436e-83e4-c31234323965" />
5.2 Отображение курса валюты:
   <img width="1146" height="514" alt="1" src="https://github.com/user-attachments/assets/8df8252d-832e-4f68-9d89-c91bbe4b70a1" />  
5.3 Страница пользователей и валют, на которые они подписаны:
   <img width="869" height="593" alt="3" src="https://github.com/user-attachments/assets/d078df6c-db1d-4d76-960b-649ae764138b" />  
<img width="1058" height="616" alt="4" src="https://github.com/user-attachments/assets/8a8b3bc7-e9f3-45fd-9812-8f21888b3f3f" />  
5.4 Страница пользователя:
   <img width="925" height="595" alt="5" src="https://github.com/user-attachments/assets/4b7801d6-ad51-4a53-bf50-2d013337a298" />
