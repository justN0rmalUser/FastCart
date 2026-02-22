from flask import current_app
from flask import request, jsonify
from app.docs_queue import start_db_cycle
import json
from flask import Flask
from flask_cors import CORS

app = Flask("FastCart")
CORS(app)
app.config.from_file('app\\config.json', load=json.load)


def api_key(auth_header: str | None):
    # Получаем ключ из заголовка Authorization
    user = current_app.config['USERS'].get(auth_header)  
    return user


@app.route('/data', methods=['POST'])
def receive_data():
    # Проверяем API-ключ
    if not api_key(request.headers.get('Auth')):
        return jsonify({"status": False, "message": "Неизвестный пользователь"}), 401
    
    material = request.get_json()
    if material:
        status, doc_title = start_db_cycle(material)
    else:
        return jsonify({"status": False, "message": "Bad request"}), 400
        
    if status:
        return jsonify({"status": True, "message": "Данные получены, обработка успешна", "title": doc_title}), 200
    
    return jsonify({"status": False, "message": "Ошибка на стороне сервера"}), 500
