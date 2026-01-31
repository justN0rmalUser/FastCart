from flask import Blueprint, current_app
from flask import request, jsonify
from docs_queue import create_doc


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
    if not api_key(request.headers.get('Auth')):
        return jsonify({"status": False, "message": "Неизвестный пользователь"}), 401

    if not request.get_json():
        return jsonify({"status": False, "message": "Пустой запрос"}), 400
    
    doc_num = create_doc(request.get_json())
    if doc_num is not None:
        return jsonify({"status": True, "message": "Данные получены, обработка успешна", "document_number": doc_num}), 200
    return jsonify({"status": False, "message": "Ошибка на стороне сервера"}), 500
