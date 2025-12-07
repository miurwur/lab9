import sqlite3
from typing import List, Optional


class DatabaseController:
    """Контроллер для работы с SQLite БД (CRUD операции)"""

    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        """Создание таблиц в БД"""
        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_code TEXT NOT NULL,
                char_code TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                value REAL,
                nominal INTEGER
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                currency_id INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user(id),
                FOREIGN KEY(currency_id) REFERENCES currency(id),
                UNIQUE(user_id, currency_id)
            )
        """)

        self.conn.commit()

    # ========== User CRUD ==========

    def create_user(self, name: str) -> int:
        """Create - добавление пользователя"""
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO user (name) VALUES (?)", (name,))
        self.conn.commit()
        return cursor.lastrowid

    def read_users(self) -> List[dict]:
        """Read - получение всех пользователей"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user")
        return [dict(row) for row in cursor.fetchall()]

    def read_user(self, user_id: int) -> Optional[dict]:
        """Read - получение пользователя по ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    # ========== Currency CRUD ==========

    def create_currency(self, currency_data: dict) -> int:
        """Create - добавление валюты"""
        sql = """
            INSERT INTO currency (num_code, char_code, name, value, nominal)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor = self.conn.cursor()
        cursor.execute(sql, (
            currency_data['num_code'],
            currency_data['char_code'],
            currency_data['name'],
            currency_data['value'],
            currency_data['nominal']
        ))
        self.conn.commit()
        return cursor.lastrowid

    def read_currencies(self) -> List[dict]:
        """Read - получение всех валют"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM currency")
        return [dict(row) for row in cursor.fetchall()]

    def read_currency(self, currency_id: int) -> Optional[dict]:
        """Read - получение валюты по ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM currency WHERE id = ?", (currency_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def update_currency(self, currency_id: int, value: float) -> bool:
        """Update - обновление курса валюты"""
        cursor = self.conn.cursor()
        cursor.execute("UPDATE currency SET value = ? WHERE id = ?", (value, currency_id))
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_currency(self, currency_id: int) -> bool:
        """Delete - удаление валюты"""
        cursor = self.conn.cursor()
        # Сначала удаляем связи
        cursor.execute("DELETE FROM user_currency WHERE currency_id = ?", (currency_id,))
        cursor.execute("DELETE FROM currency WHERE id = ?", (currency_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    # ========== User-Currency CRUD ==========

    def create_user_currency(self, user_id: int, currency_id: int) -> bool:
        """Create - добавление связи пользователь-валюта"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO user_currency (user_id, currency_id) VALUES (?, ?)",
            (user_id, currency_id)
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def read_user_currencies(self, user_id: int) -> List[dict]:
        """Read - получение валют пользователя"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT c.* FROM currency c
            JOIN user_currency uc ON c.id = uc.currency_id
            WHERE uc.user_id = ?
        """, (user_id,))
        return [dict(row) for row in cursor.fetchall()]

    def delete_user_currency(self, user_id: int, currency_id: int) -> bool:
        """Delete - удаление связи пользователь-валюта"""
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM user_currency WHERE user_id = ? AND currency_id = ?",
            (user_id, currency_id)
        )
        self.conn.commit()
        return cursor.rowcount > 0

    # ========== Инициализация тестовых данных ==========

    def init_sample_data(self):
        """Инициализация тестовых данных"""
        cursor = self.conn.cursor()

        # Проверяем, есть ли уже данные
        cursor.execute("SELECT COUNT(*) FROM currency")
        if cursor.fetchone()[0] == 0:
            # Тестовые валюты
            currencies = [
                ("840", "USD", "Доллар США", 90.5, 1),
                ("978", "EUR", "Евро", 98.2, 1),
                ("156", "CNY", "Китайский юань", 12.5, 10)
            ]
            cursor.executemany(
                "INSERT INTO currency (num_code, char_code, name, value, nominal) VALUES (?, ?, ?, ?, ?)",
                currencies
            )

        cursor.execute("SELECT COUNT(*) FROM user")
        if cursor.fetchone()[0] == 0:
            # Тестовые пользователи
            users = ["Анна", "Иван", "Мария"]
            for name in users:
                cursor.execute("INSERT INTO user (name) VALUES (?)", (name,))

        self.conn.commit()

    def close(self):
        """Закрытие соединения с БД"""
        if self.conn:
            self.conn.close()