from local_config import *
from werkzeug.security import generate_password_hash, check_password_hash
import requests


# Маршрут /signup для регистрации
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    user_id = data.get('id', None)
    password = data.get('password', None)

    if User.query.filter_by(id=user_id).first():
        return jsonify({"msg": "Пользователь с таким логином уже существует"}), 409

    # Проверяем, является ли id адресом электронной почты
    if email_regex.match(user_id):
        id_type = 'mail'
    # Проверяем, является ли id телефонным номером
    elif phone_regex.match(user_id):
        id_type = 'phone'
    else:
        return jsonify({"msg": "Неверный формат ввода ID"}), 400
    password_hash = generate_password_hash(password)

    new_user = User(id=user_id, password_hash=password_hash, id_type=id_type)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=user_id)
    return jsonify(access_token=access_token), 201


# Маршрут /signin для входа и инициализации нового Bearer токена
@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    user_id = data.get('id', None)
    password = data.get('password', None)

    user = User.query.filter_by(id=user_id).first()
    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=user_id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Неверный логин или пароль"}), 401


# Защищенный маршрут /info для вывода информации о пользователе
@app.route('/info', methods=['GET'])
@jwt_required()
def get_info():
    current_user_id, access_token = refresh_token()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"msg": "Пользователь не найден"}), 404
    return jsonify(user_id=user.id, id_type=user.id_type), 200


# Защищенный маршрут /latency, который возвращает задержку от сервиса до гугла
@app.route('/latency', methods=['GET'])
@jwt_required()
def get_latency():
    c_id, a_t = refresh_token()
    start_time = datetime.now()
    response = requests.get('https://www.google.com')
    end_time = datetime.now()
    latency = (end_time - start_time).total_seconds() * 1000  # Задержка в миллисекундах
    return jsonify(latency=latency), 200


# Защищенный маршрут /logout, который удаляет токен пользователя
@app.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # JTI (JWT ID) для текущего токена
    blacklist.add(jti)  # Добавляем JTI токена в черный список
    return jsonify(msg="Выполнен выход. Токен аннулирован (занесен в черный список)"), 200


if __name__ == '__main__':
    app.run(debug=True)
