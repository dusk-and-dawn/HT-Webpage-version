from flask import Flask, request, render_template, redirect, url_for
import sqlite3 
from datetime import datetime

#making instance of Flask app 
app = Flask(__name__)
#print(app.template_folder) keep this in case I need to debug again


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

#@app.before_first_request --> couldn't get this to ever run, maybe figure out later 
#def initialize_database():
init_db() # this solution is easy and works like a charm but might have drawback, come back here once the rest is done

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
        cur = conn.cursor()
        cur.execute('SELECT name FROM habits')
        habit_names = cur.fetchall()
        existing_habit_names = [item[0] for item in habit_names]
        for existing_habit in existing_habit_names:
            if existing_habit == name:
                streak+=1
        conn.execute('INSERT INTO habits (name, date, streak) VALUES (?, ?, ?)', (name, date, streak))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html') 

@app.route('/increment', methods=('GET', 'POST'))
def increment():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        streak = 0 
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT name FROM habits')
        habit_names = cur.fetchall()
        existing_habit_names = [item[0] for item in habit_names]
        for existing_habit in existing_habit_names:
            if existing_habit == name:
                streak+=1
        conn.execute('INSERT INTO habits (name, date, streak) VALUES (?, ?, ?)', (name, date, streak))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('increment.html') 

@app.route('/analysis', methods=('GET', 'POST'))
def analysis():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name FROM habits')
    habits = cur.fetchall()
    conn.close()
    habits_ls = [element[0] for element in habits]
    most_habit = ''
    for habit in habits_ls: 
        if habits_ls.count(habit) > habits_ls.count(most_habit):
            most_habit = habit
        elif habits_ls.count(habit) == habits_ls.count(most_habit):
            most_habit = habit, most_habit

    return render_template('analysis.html', variable_most_habit=most_habit)  

if __name__ == '__main__':
    app.run(debug= True)