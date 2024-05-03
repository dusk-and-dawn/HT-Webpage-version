import sqlite3

def get_db_connection():
    conn = sqlite3.connect('habit_tracker.db')
    conn.row_factory = sqlite3.Row # getting back dictionaries from the row data
    return conn