from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sys

# Импортируем контроллеры
from controllers.databasecontroller import DatabaseController
from controllers.currencycontroller import CurrencyController
from controllers.pages import PagesController


class Router(BaseHTTPRequestHandler):
    """
    Главный роутер приложения.
    Обрабатывает все HTTP запросы и делегирует выполнение контроллерам.
    """

    def __init__(self, *args, **kwargs):
        # Инициализация контроллеров
        self.db = DatabaseController()
        self.currency_ctrl = CurrencyController(self.db)
        self.pages = PagesController()

        # Инициализация тестовых данных
        self.db.init_sample_data()

        super().__init__(*args, **kwargs)

    # ========== Обработка GET запросов ==========

    def do_GET(self):
        """Обработка всех GET запросов"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        # Логирование запроса (для отладки)
        print(f"GET {path}", file=sys.stderr)

        try:
            # Роутинг
            if path == '/':
                self._handle_index()
            elif path == '/author':
                self._handle_author()
            elif path == '/users':
                self._handle_users()
            elif path == '/user':
                self._handle_user(query_params)
            elif path == '/currencies':
                self._handle_currencies()
            elif path == '/currency':
                self._handle_currency_form()
            elif path == '/currency/delete':
                self._handle_currency_delete(query_params)
            elif path == '/currency/update':
                self._handle_currency_update(query_params)
            elif path == '/currency/show':
                self._handle_currency_show()
            else:
                self._send_error(404, "Страница не найдена")

        except Exception as e:
            self._send_error(500, f"Внутренняя ошибка сервера: {str(e)}")

    # ========== Обработка POST запросов ==========

    def do_POST(self):
        """Обработка всех POST запросов"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        print(f"POST {path}", file=sys.stderr)

        try:
            if path == '/currency/create':
                self._handle_currency_create()
            elif path == '/user/create':  # ДОБАВЛЯЕМ
                self._handle_user_create()
            else:
                self._send_error(404, "Страница не найдена")

        except Exception as e:
            self._send_error(500, f"Ошибка: {str(e)}")

    # ========== Обработчики маршрутов ==========

    def _handle_index(self):
        """Главная страница"""
        currencies = self.currency_ctrl.list_currencies()
        html = self.pages.render_index(currencies=currencies)
        self._send_html_response(html)

    def _handle_author(self):
        """Страница об авторе"""
        html = self.pages.render_author()
        self._send_html_response(html)

    def _handle_users(self):
        """Список пользователей"""
        print(f"DEBUG: Обработка /users", file=sys.stderr)

        try:
            users = self.db.read_users()
            print(f"DEBUG: Получено пользователей: {len(users)}", file=sys.stderr)
            for i, user in enumerate(users):
                print(f"DEBUG: Пользователь {i}: {user}", file=sys.stderr)

            html = self.pages.render_users(users=users)
            print(f"DEBUG: HTML сгенерирован, длина: {len(html)}", file=sys.stderr)

            self._send_html_response(html)

        except Exception as e:
            print(f"DEBUG: Ошибка в _handle_users: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            self._send_error(500, f"Ошибка: {str(e)}")

    def _handle_user(self, params):
        """Страница пользователя"""
        user_id = int(params.get('id', [0])[0])

        if user_id:
            user = self.db.read_user(user_id)
            if user:
                currencies = self.db.read_user_currencies(user_id)
                html = self.pages.render_user(user_data=user, user_currencies=currencies)
                self._send_html_response(html)
            else:
                self._send_error(404, "Пользователь не найден")
        else:
            self._send_error(400, "Не указан ID пользователя")

    def _handle_user_create(self):
        """Создание нового пользователя (POST)"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)

        try:
            name = params['name'][0]
            user_id = self.db.create_user(name)
            print(f"DEBUG: Создан пользователь ID={user_id}, имя={name}", file=sys.stderr)
            self._send_redirect('/users')

        except (KeyError, ValueError) as e:
            self._send_error(400, f"Ошибка создания пользователя: {str(e)}")


    def _handle_currencies(self):
        """Список всех валют"""
        currencies = self.currency_ctrl.list_currencies()
        html = self.pages.render_currencies(currencies=currencies)
        self._send_html_response(html)


    def _handle_currency_delete(self, params):
        """Удаление валюты"""
        currency_id = int(params.get('id', [0])[0])

        if currency_id:
            success = self.currency_ctrl.delete_currency(currency_id)
            if success:
                self._send_redirect('/currencies')
            else:
                self._send_error(404, "Валюта не найдена")
        else:
            self._send_error(400, "Не указан ID валюты")

    def _handle_currency_update(self, params):
        """Обновление курса валюты"""
        # Ожидаем параметры вида: /currency/update?USD=95.5
        updated = False

        for param, values in params.items():
            if param.isalpha() and len(param) == 3:  # Код валюты
                char_code = param.upper()
                try:
                    new_value = float(values[0])

                    # Находим валюту по коду
                    currency = self.currency_ctrl.get_currency_by_char_code(char_code)
                    if currency:
                        success = self.currency_ctrl.update_currency_value(
                            currency['id'], new_value
                        )
                        if success:
                            updated = True

                except (ValueError, IndexError):
                    pass

        if updated:
            self._send_redirect('/currencies')
        else:
            self._send_error(400, "Не удалось обновить курс")

    def _handle_currency_show(self):
        """Вывод валют в консоль (для отладки)"""
        currencies = self.currency_ctrl.list_currencies()

        print("\n=== ВАЛЮТЫ В БАЗЕ ДАННЫХ ===")
        for currency in currencies:
            print(f"{currency['char_code']}: {currency['value']} руб.")
        print("============================\n")

        self._send_html_response("<h1>Данные выведены в консоль сервера</h1>")

    def _handle_currency_create(self):
        """Создание новой валюты"""
        print("=== DEBUG: Создание валюты ===", file=sys.stderr)

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)

        print(f"DEBUG: Получены параметры: {params}", file=sys.stderr)

        try:
            currency_data = {
                'num_code': params['num_code'][0],
                'char_code': params['char_code'][0].upper(),
                'name': params['name'][0],
                'value': float(params['value'][0]),
                'nominal': int(params['nominal'][0])
            }

            print(f"DEBUG: Данные валюты: {currency_data}", file=sys.stderr)

            # Создаем валюту
            currency_id = self.currency_ctrl.create_currency(currency_data)
            print(f"DEBUG: Валюта создана с ID={currency_id}", file=sys.stderr)

            # Проверяем, что валюта действительно добавилась
            all_currencies = self.currency_ctrl.list_currencies()
            print(f"DEBUG: Всего валют после добавления: {len(all_currencies)}", file=sys.stderr)
            for curr in all_currencies:
                print(f"DEBUG: - {curr['char_code']}: {curr['value']}", file=sys.stderr)

            # Редирект
            print("DEBUG: Делаем редирект на /currencies", file=sys.stderr)
            self._send_redirect('/currencies')

        except Exception as e:
            print(f"DEBUG: ОШИБКА: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            self._send_error(500, f"Ошибка: {str(e)}")

    # ========== Вспомогательные методы ==========

    def _send_html_response(self, html, status_code=200):
        """Отправка HTML ответа"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def _send_redirect(self, location):
        """Отправка редиректа"""
        self.send_response(302)
        self.send_header('Location', location)
        self.end_headers()

    def _send_error(self, code, message):
        """Отправка ошибки"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <body>
            <h1>Ошибка {code}</h1>
            <p>{message}</p>
            <a href="/">На главную</a>
        </body>
        </html>
        """
        self._send_html_response(html, code)


def main():
    """Запуск сервера"""
    host = 'localhost'
    port = 8080

    server = HTTPServer((host, port), Router)

    print(f"Сервер запущен на http://{host}:{port}")
    print("Доступные страницы:")
    print("  /              - Главная страница")
    print("  /author        - Об авторе")
    print("  /users         - Пользователи")
    print("  /currencies    - Валюты")
    print("  /currency/show - Отладка (вывод в консоль)")
    print("\nДля остановки сервера нажмите Ctrl+C")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
        server.server_close()


if __name__ == '__main__':
    main()