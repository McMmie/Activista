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
