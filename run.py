from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# @app.route('/', methods=['GET'])
# def home():
#     return '', 200

# @app.route('/who_work', methods=['GET'])
# def user_online():
#     if not api_key():
#         return jsonify({"status": False, "message": "Пользователь уже работает в сети"}), 401

