import sqlite3
from flask import current_app, g
'''
both current app and g are flask functionalities that make it easier to handle the database connection. 
current_app sets the configurations based on whether the App is in testing mode or production mode.
g is like a global variable but only for one request. 
'''

def get_db_connection():
    if 'db' not in g: # checks if g already holds a database and adds one otherwise 
        print('building database connection')
        g.db = sqlite3.connect(current_app.config['DATABASE']) # sets the db according to the current context 
        g.db.row_factory = sqlite3.Row # getting back dictionaries from the row data
    return g.db

def close_db_connection(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
