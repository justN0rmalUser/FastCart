import json
from flask import Flask

def create_app():
    app = Flask("FastCart")
    app.config.from_file('app\config.json', load=json.load)

    # Регистрация маршрутов
    from . import routes
    app.register_blueprint(routes.bp)

    return app