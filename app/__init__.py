import os
import datetime
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, render_template, redirect, g, flash, _app_ctx_stack
basedir = os.path.abspath(os.path.dirname(__file__))

# configuration
DATABASE = '../db/weather.db'
SECRET_KEY = 'hackerati'
DEBUG = True

# create application
app = Flask(__name__)
app.config.from_object(__name__)

# Create db tables in python shell:
def init_db():
    """Initializes the database - call from Python shell:
        >>> from __init__ import init_db
        >>> init_db()
    """
    with app.app_context():
        db = get_db()
        with app.open_resource('../sql/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    """Opens a new database connection if none open yet"""
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect(app.config['DATABASE'])
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db
    return top.sqlite_db

@app.teardown_appcontext
def close_db_connection(exception):
    """Closes the database at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()

# Routing for main page
@app.route('/', defaults={'zipcode': '11210', 'reported': '0'})
@app.route('/<zipcode>', defaults={'reported': '0'})
@app.route('/<zipcode>/<reported>')
def home(zipcode,reported):
    db = get_db()
    cursor = db.execute("select temp, humidity, stamp from weather where zipcode = %s" % (zipcode))
    results = cursor.fetchall()
    cursor.close
    return render_template('index.html', zipcode=zipcode, reported=reported, results=results)

# Route for users to report weather
@app.route('/report/<zipcode>/<temperature>/<humidity>', methods=['GET'])
def uploadfiles(zipcode,temperature,humidity):
    db = get_db()
    db.execute('insert into weather (zipcode, temp, humidity, stamp) values (?, ?, ?, ?)',
                 [zipcode, temperature, humidity, datetime.datetime.utcnow()])
    db.commit()
    flash('New entry was successfully added.')
    return redirect('/'+zipcode+'/1')

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("5001"),
        debug=True
    )
