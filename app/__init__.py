import sys
import click
from dotenv import load_dotenv
from flask import Flask, render_template
from app.config import DevelopmentConfig, TestingConfig
from app.extensions import db, limiter
from app.models import Message
from helper_functions.random_name_gen import get_random_content, get_random_name

# Load environment variables
load_dotenv()

def create_app(config=DevelopmentConfig):
    app = Flask(__name__)

    app.config.from_object(config)

    # Bind extensions to app
    db.init_app(app)
    limiter.init_app(app)

    # Create db from models if in dev/test
    if config in [DevelopmentConfig, TestingConfig]:
        with app.app_context():
            db.create_all()

    # Import and register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # Commands
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """For creating and destroying the db"""
        if drop:
            db.drop_all()
            click.echo('Database dropped.')
        db.create_all()
        click.echo('Initialized database.')
    
    @app.cli.command()
    @click.option('--num', required=True, type=int, help='Number of messages to add.')
    def forge(num):
        """ For adding messages to the db """
        if num <= 0:
            click.echo('The number of messages must be greater than 0.')
            return
        
        try:
            for _ in range(int(num)):
                m = Message(name=get_random_name(), content=get_random_content())
                db.session.add(m)
            
            db.session.commit()
            click.echo("Messages successfully added.")

        except Exception as e:
            db.session.rollback()
            click.echo(f'Something went wrong {e}')

    return app