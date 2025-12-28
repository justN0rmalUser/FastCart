from app import create_app
from app import dbuppdater
from app._utils import JSONQueue

import multiprocessing as mp


app = create_app()


if __name__ == '__main__':
    SharedQ = JSONQueue()
    server = mp.Process(target=app.run, args=('0.0.0.0', 5000, None, True))
    db_writer = mp.Process(target=dbuppdater.main)


# @app.route('/', methods=['GET'])
# def home():
#     return '', 200

# @app.route('/who_work', methods=['GET'])
# def user_online():
#     if not api_key():
#         return jsonify({"status": False, "message": "Пользователь уже работает в сети"}), 401

