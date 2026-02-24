from flask import current_app
from flask import request, jsonify
from flask import Flask
from flask_cors import CORS

from app.parse_items import create_list_items
from app.create_doc import create_document
import json


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
    
    try:
        material = request.get_json()
        
        TITLE = material["name"]
        DESCRIPTION = material["description"]
        PRODUCTS_LIST = material["products"]

        plist = create_list_items(PRODUCTS_LIST)
        doc_num = create_document(TITLE, DESCRIPTION, plist)
    except AssertionError:
        return jsonify({"status": False, "message": "Bad request"}), 400
    except Exception as exc:
        return jsonify({"status": False, "message": f"Ошибка на стороне сервера: {exc}"}), 500
    else:
        return jsonify({"status": True, "message": "Данные получены, обработка успешна", "title": TITLE, "doc_num": doc_num}), 200
