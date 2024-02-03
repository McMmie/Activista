#!/usr/bin/python3
"""
This allows one to keep track of their activities
"""
from flask import Flask


app = Flask(__name__)
@app.route('/home', strict_slashes=False)
def home_page():
    """this is the homepage"""
    return "Index page"

@app.route('/login',  strict_slashes=False)
def login():
    """goes to the login page"""
    return "login"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
