#!/bin/python3

from db import get_gb

db = get_db()
db.execute(

        'INSERT INTO users (username, email, password)'
        ' VALUES (test, test@gmail.com, 1234)')
db.commit()
