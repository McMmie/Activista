#!/bin/python3
"""connecting to sqlite database
"""
import sqlite3
import click
from flask import current app, g
from flask.cli import with_appcontext


def get_db():
    """
    initiates the database and connects to it
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
                )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    closes the connection
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db ():
    """
    a function that runs the sql commands in the schema file
    """

    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """ Clear any existing data and create new tables. """
    init_db()
    click.echo('Initializing the database')
