#!/bin/python3
"""
define a blueprint and register it in the app factory
"""

from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort
from activista.auth import login_required
from activista.db import get_db

bp = Blueprint('home', __name__)

@bp.route('/')
def landing_page():
    """landing page"""
    return render_template('landing_page.html')

@bp.route('/home', strict_slashes=False)
def index():
    """
    this is the home route which is the first page someone is lead to after
    searching for activista
    """
    db = get_db()
    posts = db.execute(
            'SELECT title, body  FROM tasks ORDER BY created ASC').fetchall()

    username = db.execute(
            'SELECT username FROM users')
    return render_template('index.html', posts=posts, username='test user')

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    """
    creats a new task
    """

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required'
        if error is not None:
            flash(error)
        else:

            db = get_db()
            db.execute(
                'INSERT INTO tasks (title, body) VALUES (?, ?)',
                (title, body)
                )
            db.commit()

            return redirect(url_for('home.index'))
        
    return render_template("create.html")
