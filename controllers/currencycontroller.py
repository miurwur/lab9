from controllers.databasecontroller import CurrencyRatesCRUD


class CurrencyController:
    """Контроллер бизнес-логики для валют"""

    def __init__(self, db_controller: CurrencyRatesCRUD):
        self.db = db_controller

    def list_currencies(self):
        return self.db._read()

    def update_currency(self, char_code: str, value: float):
        self.db._update({char_code: value})

    def delete_currency(self, currency_id: int):
        self.db._delete(currency_id)