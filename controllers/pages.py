from jinja2 import Environment, FileSystemLoader
import os


class PagesController:
    """Контроллер для рендеринга HTML страниц через Jinja2"""

    def __init__(self):
        # Получаем путь к папке templates
        templates_path = os.path.join(os.path.dirname(__file__), '..', 'templates')

        self.env = Environment(
            loader=FileSystemLoader(templates_path),
            autoescape=True
        )

    def _convert_to_dict_list(self, data_list):
        """Преобразует список объектов в список словарей"""
        if not data_list:
            return []

        result = []
        for item in data_list:
            if isinstance(item, dict):
                result.append(item)
            else:
                # Пытаемся преобразовать в словарь
                try:
                    result.append(dict(item))
                except:
                    # Если не получается, оставляем как есть
                    result.append(item)
        return result

    def render_index(self, currencies=None, author_info=None):
        """Рендер главной страницы"""
        template = self.env.get_template("index.html")

        return template.render(
            title="Главная страница",
            currencies=self._convert_to_dict_list(currencies),
            author=author_info or {"name": "Студент", "group": "P3122"}
        )

    def render_author(self):
        """Рендер страницы об авторе"""
        template = self.env.get_template("author.html")
        return template.render(
            title="Об авторе",
            author={"name": "Студент", "group": "P3122"}
        )

    def render_users(self, users=None):
        """Рендер страницы пользователей"""
        template = self.env.get_template("users.html")

        return template.render(
            title="Пользователи",
            users=self._convert_to_dict_list(users)
        )

    def render_user(self, user_data=None, user_currencies=None):
        """Рендер страницы конкретного пользователя"""
        template = self.env.get_template("user.html")

        return template.render(
            title=f"Пользователь: {user_data.get('name', 'Неизвестно') if user_data else 'Неизвестно'}",
            user=user_data if user_data else {},
            currencies=self._convert_to_dict_list(user_currencies)
        )

    def render_currencies(self, currencies=None):
        """Рендер страницы валют"""
        template = self.env.get_template("currencies.html")

        return template.render(
            title="Валюты",
            currencies=self._convert_to_dict_list(currencies)
        )