from flask import Flask, request, render_template, redirect, url_for
import sqlite3 
from datetime import datetime

#making instance of Flask app 
app = Flask(__name__)
print(app.template_folder)


def init_db():
    conn=sqlite3.connect('habit_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            streak INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

#@app.before_first_request
#def initialize_database():
init_db()

def get_db_connection():
    conn = sqlite3.connect('habit_tracker.db')
    conn.row_factory = sqlite3.Row # getting back dictionaries from the row data
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM habits')
    habits = cur.fetchall()
    conn.close()
    return render_template('index.html', habits=habits)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        name = request.form['name']
        date = datetime.now().date()
        streak = 0 

        conn = get_db_connection()
        conn.execute('INSERT INTO habits (name, date, streak) VALUES (?, ?, ?)', (name, date, streak))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html') 

if __name__ == '__main__':
    app.run(debug= True)