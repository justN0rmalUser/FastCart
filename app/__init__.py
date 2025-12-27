import json
from flask import Flask

def create_app():
    app = Flask("FastCart")
    app.config.from_file('app\config.json', load=json.load)

    # Регистрация маршрутов
    from app.routes import bp
    app.register_blueprint(bp)

    return app