# app/__init__.py

from flask import Flask
from .extensions import db, migrate
from .routes import api_bp

def create_app(config_class="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    app.register_blueprint(api_bp)

    return app
