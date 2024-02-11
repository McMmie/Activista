#!/bin/python3
"""
adds a task to the database
"""
import functools


@app.route('/new', methods=['GET', 'POST'])
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
                db =get_db()
                db.execute(
                        'INSERT INTO tasks (title, body) VALUES (?, ?, ?)',
                        (title, body)
                )
                db.commit()
                return redirect(url_for('home'))

        render_template('create.html')

