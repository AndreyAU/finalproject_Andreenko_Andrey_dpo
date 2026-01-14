import json
import argparse
from datetime import datetime
from valutatrade_hub.core.models import User
from valutatrade_hub.core.utils import load_users, save_users

def register(args):
    users = load_users()

    # Проверка на уникальность имени пользователя
    if any(user["_username"] == args.username for user in users):
        print(f"Username '{args.username}' уже занят.")
        return

    # Генерация нового user_id (по принципу автоинкремента)
    new_user_id = max([user["user_id"] for user in users], default=0) + 1

    # Создание нового пользователя
    new_user = User(new_user_id, args.username, args.password, datetime.now())
    users.append({
        "user_id": new_user._user_id,
        "username": new_user._username,
        "hashed_password": new_user._hashed_password,
        "salt": new_user._salt,
        "registration_date": new_user._registration_date.isoformat(),
    })

    save_users(users)
    print(f"Пользователь '{args.username}' зарегистрирован (id={new_user_id}). Войдите: login --username {args.username} --password <пароль>")

def login(args):
    users = load_users()

    # Поиск пользователя по username
    user = next((user for user in users if user["username"] == args.username), None)
    if not user:
        print(f"Пользователь '{args.username}' не найден.")
        return

    # Проверка пароля
    stored_password = user["hashed_password"]
    salt = user["salt"]
    if User(user["user_id"], user["username"], "", registration_date=user["registration_date"]).verify_password(args.password):
        print(f"Вы вошли как '{args.username}'")
    else:
        print("Неверный пароль")

def load_users():
    try:
        with open("data/users.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_users(users):
    with open("data/users.json", "w") as f:
        json.dump(users, f, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    # Команда register
    register_parser = subparsers.add_parser("register")
    register_parser.add_argument("--username", required=True, help="Username")
    register_parser.add_argument("--password", required=True, help="Password")
    register_parser.set_defaults(func=register)

    # Команда login
    login_parser = subparsers.add_parser("login")
    login_parser.add_argument("--username", required=True, help="Username")
    login_parser.add_argument("--password", required=True, help="Password")
    login_parser.set_defaults(func=login)

    args = parser.parse_args()
    args.func(args)

