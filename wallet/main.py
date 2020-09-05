from werkzeug.exceptions import HTTPException

from flask import Flask
from flask_migrate import Migrate

from wallet.utils import register_handlers
from wallet.errors import handle_exception


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_error_handler(HTTPException, handle_exception)

    from wallet.api import api
    app.register_blueprint(api)

    from wallet.db import db
    db.init_app(app)
    Migrate(app, db)

    register_handlers(app)
    return app
