from urllib.parse import parse_qs, urlparse
from jinja2 import Environment, PackageLoader, select_autoescape
from http.server import HTTPServer, BaseHTTPRequestHandler

# Импорты моделей
from models import Users_id, CurrencyID, get_currencies, Currencies_users

# Импорты контроллеров
from controllers.databasecontroller import CurrencyRatesCRUD
from controllers.currencycontroller import CurrencyController

# Инициализация
db_crud = CurrencyRatesCRUD()
currency_controller = CurrencyController(db_crud)

# Навигационное меню
NAVIGATION_page2 = [
    {"caption": "Главная", "href": "/"},
    {"caption": "Курсы валют", "href": "/currency"},
    {"caption": "Пользователи и валюты", "href": "/users_currencies"}
]

# Настройка Jinja2
env = Environment(
    loader=PackageLoader("my_App"),
    autoescape=select_autoescape()
)


# Инициализация БД
def init_database():
    """Добавить тестовые данные, если БД пуста"""
    cursor = db_crud.connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM currency")
    if cursor.fetchone()[0] == 0:
        print("Инициализация БД: добавление тестовых валют...")
        db_crud.add_test_currencies()
    cursor.close()


init_database()


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    user_data = None

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

        # Главная страница
        if path == '/':
            template = env.get_template("page1.html")
            result = template.render(title="Введите ваши данные", user_data=None)
            self.wfile.write(bytes(result, "utf-8"))

        elif path == '/users_currencies':
            """Страница с пользователями и валютами"""
            template = env.get_template("currencies_users.html")

            try:
                # Получаем всех пользователей
                cursor = db_crud.connection.cursor()
                cursor.execute("SELECT * FROM user")
                users = [dict(row) for row in cursor.fetchall()]

                # Для каждого пользователя получаем его валюты
                for user in users:
                    cursor.execute("""
                        SELECT c.* FROM currency c
                        JOIN user_currency uc ON c.id = uc.currency_id
                        WHERE uc.user_id = ?
                    """, (user['id'],))
                    user['currencies'] = [dict(row) for row in cursor.fetchall()]

                cursor.close()

                result = template.render(
                    title="Пользователи и валюты",
                    navigation=NAVIGATION_page2,
                    users_data=users,
                    error=query_params.get('error', [None])[0],
                    message=query_params.get('message', [None])[0]
                )
                self.wfile.write(bytes(result, "utf-8"))

            except Exception as e:
                print(f"Ошибка страницы пользователей: {e}")
                result = template.render(
                    title="Ошибка",
                    navigation=NAVIGATION_page2,
                    users_data=[],
                    error=f"Ошибка загрузки: {str(e)}"
                )
                self.wfile.write(bytes(result, "utf-8"))

        # Страница валют (CRUD - Read)
        elif path == '/currency':
            template = env.get_template("currency_input.html")
            currencies = currency_controller.list_currencies()

            result = template.render(
                title="Курсы валют",
                navigation=NAVIGATION_page2,
                currencies=currencies,
                message=query_params.get('message', [None])[0],
                error=query_params.get('error', [None])[0]
            )
            self.wfile.write(bytes(result, "utf-8"))

        # Удаление валюты (CRUD - Delete)
        elif path == '/currency/delete':
            if 'id' in query_params:
                try:
                    currency_id = int(query_params['id'][0])
                    currency_controller.delete_currency(currency_id)
                except:
                    pass

            self.send_response(302)
            self.send_header('Location', '/currency')
            self.end_headers()

        # Обновление курса (CRUD - Update)
        elif path == '/currency/update':
            # Обработка запросов: /currency/update?USD=95.0
            if query_params:
                for key, values in query_params.items():
                    if len(key) == 3:  # код валюты
                        try:
                            currency_controller.update_currency(key.upper(), float(values[0]))
                            print(f"Обновлен курс {key} = {values[0]}")
                        except:
                            pass

            self.send_response(302)
            self.send_header('Location', '/currency')
            self.end_headers()


        elif path == '/load_cbr_rates':
            """Загрузка актуальных курсов от ЦБ РФ"""
            try:
                from models.currency import get_currencies

                # Получаем популярные валюты
                popular_codes = ['USD', 'EUR', 'GBP', 'CNY', 'JPY', 'CHF']
                actual_rates = get_currencies(popular_codes)

                updated_count = 0
                for char_code, data in actual_rates.items():
                    if isinstance(data, dict):  # если это данные, а не ошибка
                        # Обновляем курс в БД
                        currency_controller.update_currency(char_code, float(data['value']))
                        updated_count += 1

                message = f"Обновлено {updated_count} курсов от ЦБ РФ"
                print(message)

                self.send_response(302)
                self.send_header('Location', f'/currency?message={message}')
                self.end_headers()

            except Exception as e:
                print(f"Ошибка загрузки курсов ЦБ: {e}")
                self.send_response(302)
                self.send_header('Location', f'/currency?error=Ошибка загрузки: {str(e)}')
                self.end_headers()

        # Страница конкретной валюты
        elif path.startswith('/currency/') and path != '/currency/':
            currency_code = path.split('/')[-1]
            template = env.get_template("currency_result.html")

            # Ищем валюту
            currency_data = None
            currencies = currency_controller.list_currencies()
            for curr in currencies:
                if curr['char_code'].upper() == currency_code.upper():
                    currency_data = curr
                    break

            if currency_data:
                result = template.render(
                    title=f"Курс {currency_code}",
                    navigation=NAVIGATION_page2,
                    currency_id=currency_code,
                    currency_name=currency_data['name'],
                    rate=currency_data['value'],
                    nominal=currency_data['nominal'],
                    error=None
                )
            else:
                result = template.render(
                    title=f"Курс {currency_code}",
                    navigation=NAVIGATION_page2,
                    currency_id=currency_code,
                    error="Валюта не найдена"
                )

            self.wfile.write(bytes(result, "utf-8"))

        elif path == '/user':
            """Страница конкретного пользователя"""
            if 'id' in query_params:
                try:
                    user_id = int(query_params['id'][0])

                    # Получаем информацию о пользователе
                    cursor = db_crud.connection.cursor()
                    cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))
                    user_row = cursor.fetchone()

                    if user_row:
                        user_data = dict(user_row)

                        # Получаем валюты пользователя
                        cursor.execute("""
                            SELECT c.* FROM currency c
                            JOIN user_currency uc ON c.id = uc.currency_id
                            WHERE uc.user_id = ?
                        """, (user_id,))
                        user_currencies = [dict(row) for row in cursor.fetchall()]

                        cursor.close()

                        # Рендерим шаблон
                        template = env.get_template("user_page.html")
                        result = template.render(
                            title=f"Пользователь: {user_data['name']}",
                            navigation=NAVIGATION_page2,
                            user=user_data,
                            currencies=user_currencies
                        )
                        self.wfile.write(bytes(result, "utf-8"))
                    else:
                        self.send_response(302)
                        self.send_header('Location', '/users_currencies?error=Пользователь не найден')
                        self.end_headers()

                except Exception as e:
                    print(f"Ошибка страницы пользователя: {e}")
                    self.send_response(302)
                    self.send_header('Location', f'/users_currencies?error={str(e)}')
                    self.end_headers()
            else:
                self.send_response(302)
                self.send_header('Location', '/users_currencies?error=Не указан ID пользователя')
                self.end_headers()

        # Тестовые маршруты для проверки CRUD
        elif path == '/add_test_data':
            """Добавить тестовые валюты"""
            db_crud.add_test_currencies()
            self.send_response(302)
            self.send_header('Location', '/currency?message=Тестовые валюты добавлены')
            self.end_headers()

        elif path == '/clear_data':
            """Очистить БД (для тестирования)"""
            cursor = db_crud.connection.cursor()
            cursor.execute("DELETE FROM currency")
            db_crud.connection.commit()
            cursor.close()
            self.send_response(302)
            self.send_header('Location', '/currency?message=БД очищена')
            self.end_headers()

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # Обработка формы пользователя
        if path == '/submit':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                data = parse_qs(post_data)

                name = data['name'][0]
                age = int(data['age'][0])
                email = data['email'][0]

                self.user_data = Users_id(name, age, email)

                # Сохраняем в БД
                cursor = db_crud.connection.cursor()
                cursor.execute(
                    "INSERT INTO user(name, age, email) VALUES(?, ?, ?)",
                    (name, age, email)
                )
                db_crud.connection.commit()
                cursor.close()

                self.send_response(302)
                self.send_header('Location', '/currency')
                self.end_headers()

            except ValueError as e:
                template = env.get_template("page1.html")
                result = template.render(
                    title="Введите ваши данные",
                    user_data=None,
                    error=str(e)
                )
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(bytes(result, "utf-8"))

        # Обработка формы поиска валюты
        elif path == '/currency_submit':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = parse_qs(post_data)

            currency_code = data['currency_code'][0].strip()

            try:
                currency_obj = CurrencyID(currency_code)
                self.send_response(302)
                self.send_header('Location', f'/currency/{currency_obj.id}')
                self.end_headers()
            except ValueError as e:
                template = env.get_template("currency_input.html")
                currencies = currency_controller.list_currencies()
                result = template.render(
                    title="Курсы валют",
                    navigation=NAVIGATION_page2,
                    currencies=currencies,
                    error=str(e)
                )
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(bytes(result, "utf-8"))


        # В do_POST, в блоке path == '/add_currency':
        elif path == '/add_currency':
            """Добавление валюты для пользователя"""
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                data = parse_qs(post_data)

                username = data['username'][0]
                currency_code = data['currency'][0].strip().upper()

                # 1. Находим или создаем пользователя
                cursor = db_crud.connection.cursor()
                cursor.execute("SELECT id FROM user WHERE name = ?", (username,))
                user_row = cursor.fetchone()

                if user_row:
                    user_id = user_row[0]
                else:
                    # Создаем нового пользователя
                    cursor.execute(
                        "INSERT INTO user(name, age, email) VALUES(?, ?, ?)",
                        (username, 25, f"{username}@example.com")
                    )
                    user_id = cursor.lastrowid

                # 2. Находим валюту
                cursor.execute("SELECT id FROM currency WHERE char_code = ?", (currency_code,))
                currency_row = cursor.fetchone()

                if currency_row:
                    currency_id = currency_row[0]

                    # 3. Добавляем связь (если её нет)
                    cursor.execute("""
                        INSERT OR IGNORE INTO user_currency(user_id, currency_id) 
                        VALUES(?, ?)
                    """, (user_id, currency_id))

                    db_crud.connection.commit()
                    cursor.close()

                    message = f"Пользователь {username} подписан на {currency_code}"
                    print(message)

                    self.send_response(302)
                    self.send_header('Location', f'/users_currencies?message={message}')
                    self.end_headers()
                else:
                    cursor.close()
                    self.send_response(302)
                    self.send_header('Location', f'/users_currencies?error=Валюта {currency_code} не найдена')
                    self.end_headers()

            except Exception as e:
                print(f"Ошибка добавления подписки: {e}")
                self.send_response(302)
                self.send_header('Location', f'/users_currencies?error={str(e)}')
                self.end_headers()




# Запуск сервера
if __name__ == '__main__':
    httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    print('=' * 50)
    print('Сервер запущен: http://localhost:8080')
    print('-' * 50)
    print('Доступные маршруты:')
    print('  /currency            - список валют (CRUD)')
    print('  /currency/update?USD=95.0  - обновить курс')
    print('  /currency/delete?id=1      - удалить валюту')
    print('  /add_test_data       - добавить тестовые данные')
    print('  /clear_data          - очистить БД')
    print('=' * 50)
    httpd.serve_forever()