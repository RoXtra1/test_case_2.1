from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
from datetime import datetime, timedelta
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)
# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/test_case'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Конфигурация JWT
app.config['JWT_SECRET_KEY'] = 'secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=10)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Регулярные выражения для проверки номера телефона и email
phone_regex = re.compile(r'^\+?d{10,12}$')
email_regex = re.compile(r'^\S+@[a-z]+.[a-z]+$')


# Модель пользователя
class User(db.Model):
    id = db.Column(db.String(120), primary_key=True)
    password_hash = db.Column(db.Text)
    id_type = db.Column(db.String(10))  # 'phone' или 'mail'

    def __init__(self, id, password_hash, id_type):
        self.id = id
        self.password_hash = password_hash
        self.id_type = id_type


# Создание таблицы в базе данных
with app.app_context():
    db.create_all()


# Список для хранения JTI отозванных токенов
blacklist = set()


# Проверка, находится ли JTI в черном списке
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in blacklist


def refresh_token():
    cur_id = get_jwt_identity()
    acc_tok = create_access_token(identity=cur_id)
    return cur_id, acc_tok
