#!/bin/python3

"""this is the main app
The flask module that imports routes the all the web pages"""

from flask import Flask
from flask import render_template
from flask import request
from markupsafe import escape
from flask import redirect, url_for


app = Flask(__name__)

@app.route('/', strict_slashes=False)
def landing_page():
    """
    this is the home route which is the first page someone is lead to after
    searching for activista
    """

    return render_template('landing_page.html')

@app.route('/login', methods=['GET', 'POST'],  strict_slashes=False)
def login():
    """
    leads to the login page where user can enter their information  and it
    is then checked if user exists in the database
    """
    users = {'test@gmail.com':'1234', 'test1@gmail.com':'1233'}
    error = None

    if request.method == 'POST':
        user = request.form['username']
        passwd = request.form['password']
        if user in users and users[user] == passwd:
            return redirect('/')

        else:
            error = 'Invalid user credentials!'
    return render_template('login.html', error=error)


@app.route('/<username>', strict_slashes=False)
def user_account(username):
    """
    displays user info and their account
    """
    if username == 'landing_page.html':
        redirect('/')

    username = username.replace('.html', '')
    if username != 'Sam':
        try:
            return redirect(url_for('%s' %escape(username)))
        except:
            return '<h2>User does not exist....quit playin man</h2>'
    else:
        return 'User %s' %escape(username)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
