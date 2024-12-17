from dotenv import load_dotenv
from flask import Flask, render_template
from hive.config import DevelopmentConfig, TestingConfig
from hive.core.commands import register_commands
from hive.core.extensions import db, bootstrap
from hive.models import Message
from hive.blueprints.main import main_bp

# Load environment variables
load_dotenv()

def create_app(config=DevelopmentConfig):
    app = Flask(__name__)

    app.config.from_object(config)

    # Bind extensions to app
    db.init_app(app)
    bootstrap.init_app(app)

    # Create db from models if in dev/test
    if config in [DevelopmentConfig, TestingConfig]:
        with app.app_context():
            db.create_all()

    # Import and register blueprints
    app.register_blueprint(main_bp)

    register_commands(app)

    return app