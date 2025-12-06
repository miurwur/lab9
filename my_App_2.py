from jinja2 import Environment, PackageLoader, select_autoescape
from models.author import Author
from models.app import App
from models.user import User
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import datetime
import json
from controllers .currencycontroller import get_currencies
from models.user_currency import UserCurrency
from models.currency import Currency
from api import Api, MockApi, ApplicationApi


# Инициализация Jinja2
env = Environment(
    loader=PackageLoader("my_App_2"),
    autoescape=select_autoescape()
)

main_author = Author('Роза Тихонова', 'P3122')


main_app = App(
    name="CurrenciesListApp",
    version="1.0.0",
    author = main_author
)

api: Api = ApplicationApi()

class MyHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Обработка GET-запросов"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        # Устанавливаем общие заголовки
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

        # Обработка разных маршрутов
        response_html = ""

        if path == "/" or path == "/index.html":
            # Главная страница
            template = env.get_template("index.html")
            response_html = template.render(
                myapp=main_app.name,
                author_name=main_author.name,
                group=main_author.group,
                navigation=[
                    {'caption': 'Основная страница', 'href': '/'},
                ],
            )

        elif path == "/users":
            # Загружаем users.html - отдельный файл
            template = env.get_template("users.html")
            response_html = template.render(
                myapp="CurrenciesListApp",
                users=api.get_users(),
                author_name=main_author.name,
            )

        elif path == "/currencies":
            # Загружаем currencies.html - отдельный файл
            template = env.get_template("currencies.html")
            currencies = api.get_currencies()

            response_html = template.render(
                myapp="CurrenciesListApp",
                author_name=main_author.name,
                currencies=currencies,
            )

        elif path.startswith("/user"):
            # Загружаем user_detail.html - отдельный файл
            user_id = int(query_params['id'][0])
            user = next((u for u in api.get_users() if u.id == user_id), None)
            user_currencies = tuple(c.id for c in api.get_user_currencies() if c.user_id == user_id)
            currencies = tuple(c for c in api.get_currencies() if c.id in user_currencies)

            template = env.get_template("user_detail.html")
            response_html = template.render(
                myapp="CurrenciesListApp",
                user=user,
                author_name=main_author.name,
                currencies=currencies
            )

        elif path == "/author":
            template = env.get_template("author.html")
            response_html = template.render(
                myapp="CurrenciesListApp",
                author = main_author,
            )

        elif path == "/api/users":
            users_data = [
                {"id": user.id, "name": user.name}
                for user in api.get_users()
            ]
            template = env.get_template('users.html')
            response_html = template.render(
                myapp="CurrenciesListApp",
                author=main_author,
                users=users_data
            )

        else:
            # 404
            template = env.get_template("index.html")
            response_html = template.render(
                myapp=main_app.name,
                author_name=main_author.name,
                group=main_author.group,
                navigation=[
                    {'caption': 'На главную', 'href': '/'},
                    {'caption': 'Пользователи', 'href': '/users'}
                ],
                page_title="404 - Страница не найдена",
                message=f"Страница {path} не существует"
            )

        # Отправляем ответ
        self.wfile.write(response_html.encode('utf-8'))

def run_server(port=8080):
    server_address = ('localhost', port)
    httpd = HTTPServer(server_address, MyHTTPRequestHandler)

    print(f"""
    Сервер запущен на http://localhost:{port}
    Доступные маршруты:

    • /              - Главная страница
    • /users         - Список пользователей
    • /currencies    - Курсы валют
    • /author        - Информация об авторе
    • /api/users     - API пользователей (JSON)

    Для остановки нажмите Ctrl+C
    """)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
        httpd.server_close()

if __name__ == "__main__":
    run_server(8080)