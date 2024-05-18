import sqlite3
from flask import current_app



def get_db_connection():
    conn = sqlite3.connect(current_app.config['DATABASE'])
    conn.row_factory = sqlite3.Row # getting back dictionaries from the row data
    return conn