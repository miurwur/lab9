import sqlite3
from contextlib import closing


class CurrencyRatesCRUD:
    """Контроллер для работы с SQLite БД (низкоуровневый)"""

    def __init__(self, db_path=':memory:'):
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        """Создание таблиц"""
        with closing(self.connection.cursor()) as cursor:
            # Таблица валют
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS currency (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    num_code TEXT NOT NULL,
                    char_code TEXT NOT NULL,
                    name TEXT NOT NULL,
                    value REAL,
                    nominal INTEGER
                )
            """)
            # Таблица пользователей
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    email TEXT NOT NULL
                )
            """)
            # Таблица связи пользователь-валюта
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_currency (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    currency_id INTEGER NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES user(id),
                    FOREIGN KEY(currency_id) REFERENCES currency(id)
                )
            """)
            self.connection.commit()

    def _create(self, data):
        """Create - добавление валюты"""
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("""
                INSERT INTO currency(num_code, char_code, name, value, nominal)
                VALUES(:num_code, :char_code, :name, :value, :nominal)
            """, data)
            self.connection.commit()
            return cursor.lastrowid

    def _read(self):
        """Read - чтение всех валют"""
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM currency ORDER BY char_code")
            return [dict(row) for row in cursor.fetchall()]

    def _update(self, updates):
        """Update - обновление курсов валют. updates = {'USD': 95.0}"""
        with closing(self.connection.cursor()) as cursor:
            for char_code, new_value in updates.items():
                cursor.execute(
                    "UPDATE currency SET value = ? WHERE UPPER(char_code) = UPPER(?)",
                    (new_value, char_code)
                )
            self.connection.commit()
        return True

    def _delete(self, currency_id):
        """Delete - удаление валюты по ID"""
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("DELETE FROM currency WHERE id = ?", (currency_id,))
            self.connection.commit()
            return cursor.rowcount > 0

    def add_test_currencies(self):
        """Добавить тестовые валюты """
        test_data = [
            {"num_code": "840", "char_code": "USD", "name": "Доллар США", "value": 90.0, "nominal": 1},
            {"num_code": "978", "char_code": "EUR", "name": "Евро", "value": 100.0, "nominal": 1},
            {"num_code": "826", "char_code": "GBP", "name": "Фунт стерлингов", "value": 115.0, "nominal": 1}
        ]
        for data in test_data:
            self._create(data)
        print(f"Добавлено {len(test_data)} тестовых валют")