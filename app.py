import os

from flask import Flask

from navigation import NAV_ITEMS
from database import init_db
from routes.main import main_bp
from routes.admin import admin_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    server_name = os.environ.get("SERVER_NAME")
    if server_name:
        app.config["SERVER_NAME"] = server_name

    @app.context_processor
    def inject_navigation():
        return {"nav_items": NAV_ITEMS}

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        init_db()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
