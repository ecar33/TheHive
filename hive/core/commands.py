import click
from hive.lorem import get_random_body, get_random_name
from hive.core.extensions import db
from hive.models import Message

def register_commands(app):
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
                m = Message(name=get_random_name(), body=get_random_body())
                db.session.add(m)
            
            db.session.commit()
            click.echo("Messages successfully added.")

        except Exception as e:
            db.session.rollback()
            click.echo(f'Something went wrong {e}')
