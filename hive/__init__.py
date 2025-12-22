import os
import sys
from math import ceil

import humanize
from dotenv import load_dotenv
from flask import Flask

from hive.blueprints.auth import auth_bp
from hive.blueprints.main import main_bp
from hive.blueprints.message import message_bp
from hive.config import DevelopmentConfig, ProductionConfig, TestingConfig
from hive.core.commands import register_commands
from hive.core.errors import register_errors
from hive.core.extensions import bcrypt, crsf, db, limiter, login_manager, migrate
from hive.models import Message, User

# Load environment variables
load_dotenv()

WIN = sys.platform.startswith('win')

def create_app(config_class=None):
    app = Flask(__name__)

    # Config selection
    if config_class is not None:
        config = config_class
        app.config.from_object(config_class)
    else:
        env = os.getenv("FLASK_CONFIG", "development")

        config_map = {
            "development": DevelopmentConfig,
            "testing": TestingConfig,
            "production": ProductionConfig,
        }

        config = config_map[env]
        app.config.from_object(config)

    # Bind extensions to app
    db.init_app(app)
    limiter.init_app(app)
    bcrypt.init_app(app)
    crsf.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    print(f'DB is: {app.config["SQLALCHEMY_DATABASE_URI"]}')

    # Import and register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(message_bp)

    register_commands(app)
    register_errors(app)

    @app.context_processor
    def utility_processor():
        def get_timedelta_string(message: Message):
            td = message.time_since_creation()
            return humanize.naturaldelta(td)
        def count_pages():
            stmnt = db.select(Message)
            result = db.session.execute(stmnt).scalars().all()
            return int(ceil(len(result)/100))
        return dict(get_timedelta_string=get_timedelta_string, count_pages=count_pages)
    
    return app

@login_manager.user_loader
def load_user(user_id):
    user = db.session.execute(db.select(User).where(User.id == user_id)).scalars().first()
    return user