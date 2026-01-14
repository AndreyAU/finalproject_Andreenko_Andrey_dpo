import hashlib
import os
from datetime import datetime

class User:
    def __init__(self, user_id, username, password, registration_date=None):
        self._user_id = user_id
        self._username = username
        self._salt = os.urandom(16).hex()  # Генерация уникальной соли
        self._hashed_password = self._hash_password(password)
        self._registration_date = registration_date or datetime.now()

    def _hash_password(self, password):
        # Хеширование пароля с солью
        return hashlib.sha256((password + self._salt).encode()).hexdigest()

    def get_user_info(self):
        # Возвращаем информацию о пользователе без пароля
        return {
            "user_id": self._user_id,
            "username": self._username,
            "registration_date": self._registration_date.isoformat()
        }

    def change_password(self, new_password):
        # Изменяем пароль
        self._hashed_password = self._hash_password(new_password)

    def verify_password(self, password):
        # Проверяем введённый пароль
        return self._hashed_password == self._hash_password(password)

class Wallet:
    def __init__(self, currency_code):
        self.currency_code = currency_code
        self._balance = 0.0

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Balance must be a number.")
        if value < 0:
            raise ValueError("Balance cannot be negative.")
        self._balance = value

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise ValueError("Insufficient balance.")
        self._balance -= amount

    def get_balance_info(self):
        return f"Currency: {self.currency_code}, Balance: {self._balance:.2f}"

class Portfolio:
    def __init__(self, user_id):
        self._user_id = user_id
        self._wallets = {}

    def add_currency(self, currency_code):
        if currency_code in self._wallets:
            raise ValueError(f"Wallet for {currency_code} already exists.")
        self._wallets[currency_code] = Wallet(currency_code)

    def get_total_value(self, base_currency='USD'):
        total_value = 0.0
        # Используем фиктивные курсы для конвертации
        exchange_rates = {
            'USD': 1.0,
            'BTC': 60000.0,  # Примерный курс BTC
            'EUR': 1.2,      # Примерный курс EUR
        }

        for wallet in self._wallets.values():
            balance = wallet.balance
            rate = exchange_rates.get(wallet.currency_code, 1.0)
            total_value += balance * rate

        return total_value

    def get_wallet(self, currency_code):
        return self._wallets.get(currency_code)

    @property
    def user(self):
        return self._user_id

    @property
    def wallets(self):
        return self._wallets.copy()


