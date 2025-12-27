from flask import Blueprint, current_app
from flask import request, jsonify
from pprint import pprint


bp = Blueprint(
    'main',         # ← Blueprint name (must be unique in the app)
    __name__        # ← Import name (usually __name__)
)


def api_key(auth_header: str | None):
    # Получаем ключ из заголовка Authorization
    user = current_app.config['USERS'].get(auth_header)  
    return user

@bp.route('/data', methods=['POST'])
def receive_data():
    # Проверяем API-ключ
    key = request.headers.get('Authorization')
    if not api_key(key):
        return jsonify({"status": False, "message": "Неизвестный пользователь"}), 401

    data = request.get_json()
    #TODO логику
    pprint(data)
    return jsonify({"status": True, "message": "Данные получены"}), 200

