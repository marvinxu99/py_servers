import sqlite3
from datetime import datetime

import click
from flask import current_app, g


# Define a custom converter function for timestamps
def parse_timestamp(value):
    return datetime.strptime(value.decode("utf-8"), "%Y-%m-%d %H:%M:%S")


def get_db():
    if 'db' not in g:
        # Register the custom timestamp converter
        sqlite3.register_converter("timestamp", parse_timestamp)

        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


# registered with the application instance
def init_app(app):
    # registered the functions with the application instance
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)   # Register init-db() with the app so it can be called using the flask command, similar to the run command
