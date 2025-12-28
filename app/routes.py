from flask import Blueprint, current_app
from flask import request, jsonify
from queue_thread import append_to_queue, db_write


bp = Blueprint(
    'main',         # ← Blueprint name (must be unique in the app)
    __name__        # ← Import name (usually __name__)
)
HEAD = request.headers


def api_key(auth_header: str | None):
    # Получаем ключ из заголовка Authorization
    user = current_app.config['USERS'].get(auth_header)  
    return user

@bp.route('/data', methods=['POST'])
def receive_data():
    # Проверяем API-ключ
    if not api_key(HEAD.get('Auth')):
        return jsonify({"status": False, "message": "Неизвестный пользователь"}), 401

    append_to_queue(request.get_json())
    return jsonify({"status": True, "message": "Данные получены, идет обработка"}), 204

@bp.route('/data/check', methods=['GET'])
def check_dbwork():
    # Проверяем API-ключ
    if not api_key(HEAD.get('Auth')):
        return jsonify({"status": False, "message": "Неизвестный пользователь"}), 401

    


