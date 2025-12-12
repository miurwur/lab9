# controllers/pages.py
from jinja2 import Environment, PackageLoader


class PageRenderer:
    """Контроллер для рендеринга страниц"""

    def __init__(self):
        self.env = Environment(
            loader=PackageLoader("my_App"),
            autoescape=select_autoescape()
        )

    def render_currency_page(self, currencies: list, message: str = None, error: str = None):
        """Рендерит страницу с валютами"""
        template = self.env.get_template("currency_input.html")
        return template.render(
            title="Курсы валют",
            navigation=NAVIGATION_page2,
            currencies=currencies,
            message=message,
            error=error
        )

    def render_user_page(self, users_data: list, error: str = None):
        """Рендерит страницу пользователей"""
        template = self.env.get_template("currencies_users.html")
        return template.render(
            title="Пользователи и валюты",
            navigation=NAVIGATION_page2,
            users_data=users_data,
            error=error
        )