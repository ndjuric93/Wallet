from wallet.db import db


def register_handlers(app):
    """
    Register all custom handlers to flask app.
    """

    @app.after_request
    def db_commit(response):
        """
        Final session commit, execute on after each request
        """
        db.session.commit()
        return response
