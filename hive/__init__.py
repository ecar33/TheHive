from math import ceil
import os
import sys
from dotenv import load_dotenv
from flask import Flask, render_template
import humanize
from hive.config import DevelopmentConfig, ProductionConfig, TestingConfig
from hive.core.commands import register_commands
from hive.core.errors import register_errors
from hive.core.extensions import db
from hive.models import Message
from hive.blueprints.main import main_bp
from hive.blueprints.message import message_bp

# Load environment variables
load_dotenv()

WIN = sys.platform.startswith('win')

def create_app(config=None):
    app = Flask(__name__)

    app.config.from_object(config)
    
    if config == ProductionConfig:

        db_file_path = os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))

        if WIN:
            db_file_path = db_file_path.replace('\\', '/')

        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file_path

    # Bind extensions to app
    db.init_app(app)

    print(f'DB is: {app.config["SQLALCHEMY_DATABASE_URI"]}')

    # Create db from models if in dev/test
    if config in [DevelopmentConfig, TestingConfig]:
        with app.app_context():
            db.create_all()

    # Import and register blueprints
    app.register_blueprint(main_bp)
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