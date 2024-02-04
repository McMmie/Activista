#!/bin/python3

"""this is the main app
The flask module that imports routes the all the web pages"""

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def landing_page():
    """
    this is the home route which is the first page someone is lead to after
    searching for activista
    """

    return render_template('landing_page.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
