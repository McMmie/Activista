#!/bin/python3
"""
authentication module
"""

import functools
from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for)

from werkzeug.security import check_password_hash, generate_password_hash
from activista.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT user_id FROM users WHERE username = ? OR email = ?', (username, email,)
            ).fetchone() is not None:
                error = 'User {} exists.'.format(username)

        if error is None:
            db.execute(
                    'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                    (username, email, generate_password_hash(password)))
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    leads to the login page where user can enter their information  and it
    is then checked if user exists in the database
    """

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        
        users = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()
        
        if users is None:
            error = 'Incorrect username.'
        elif not check_password_hash(users['password'], password):
            error = 'Incorrect password.'
        
        if error is None:
            session.clear()
            session['user_id'] = users['user_id']
            return redirect(url_for('home.index'))
        
        flash(error)
    
    return render_template('/login.html')

@bp.before_app_request
def load_user():
    """
    loads user info after loging in
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
                'SELECT * FROM users WHERE user_id = ?', (user_id,)
                ).fetchone()

@bp.route('/logout')
def logout():
    """
    logs out a user
    """
    session.clear()
    return redirect('/')

def login_required(view):
    """
    require authentication in other views
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
