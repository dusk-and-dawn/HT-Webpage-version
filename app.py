from flask import Flask, request, render_template, redirect, url_for, current_app, g
import sqlite3 
from datetime import datetime
from analysis import current_streak
from database import get_db_connection, close_db_connection

#making instance of Flask app 
app = Flask(__name__)
app.config['DATABASE'] = 'habit_tracker.db'

def init_db():
    with app.app_context():
        database_path = app.config.get('DATABASE', 'habit_tracker.db')
        conn=sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                streak INTEGER,
                periodicity TEXT NOT NULL
            )
        ''')

        # Check if the column periodicity exists
        cur.execute("PRAGMA table_info(habits)")
        columns = [column[1] for column in cur.fetchall()]
        if 'periodicity' not in columns:
            cur.execute('ALTER TABLE habits ADD COLUMN periodicity TEXT NOT NULL DEFAULT "daily"')

        conn.commit()
        conn.close()
        
@app.before_request
def before_request():
    g.db = get_db_connection()


# This closes the connection after each request: 
@app.teardown_appcontext
def teardown(exception):
    close_db_connection(exception)

#@app.before_first_request --> couldn't get this to ever run, maybe figure out later 
#def initialize_database():

init_db() # this solution is easy and works like a charm but might have drawbacks, come back here once the rest is done

@app.route('/')
def index():
    app.config['DATABASE']  = 'habit_tracker.db'
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM habits')
    habits = cur.fetchall()
    #conn.close()
    return render_template('index.html', habits=habits)

@app.route('/add', methods=('GET', 'POST'))
def add():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name FROM habits')
    existing_stuff = cur.fetchall()
    #existing_stuff_names = [item[0] for item in habit_names]
    if request.method == 'POST':
        if 'name' in request.form:
            name = request.form['name']
            periodicity = request.form['periodicity']
            date = datetime.now().date()
            #streak = 1 
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT name FROM habits')
            habit_names = cur.fetchall()
            existing_habit_names = [item[0] for item in habit_names]
            for existing_habit in existing_habit_names:
                if existing_habit == name:
                    return 'this habit already exists, please insert a new habit, or increment the existing one', 500
            conn.execute('INSERT INTO habits (name, date, periodicity) VALUES (?, ?, ?)', (name, date, periodicity))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        else: 
            return "error no name provided", 400 
    return render_template('add.html', habits = set(existing_stuff)) 

@app.route('/increment', methods=('POST', 'GET'))
def increment():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name FROM habits')
    habit_names = cur.fetchall()
    existing_habit_names = [item[0] for item in habit_names]
    options = list(set(existing_habit_names))
    conn.close()
    return render_template('increment.html', options=options)

@app.route('/submit-dropdown', methods=('GET', 'POST'))
def handle_dropdown():
    name = request.form['dropdown']
    conn = get_db_connection()
    cur = conn.cursor()
    date = datetime.now().date()
    cur.execute('SELECT periodicity FROM habits WHERE name = ?', (name,))
    habit_per = cur.fetchone()[0]
    conn.execute('INSERT INTO habits (name, date, periodicity) VALUES (?, ?, ?)', (name, date, habit_per))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/record-alternative-date', methods=('POST', 'GET'))
def record_alternative_date():
    name = request.form['dropdown']
    conn = get_db_connection()
    cur = conn.cursor() 
    date = request.form['date']
    cur.execute('SELECT periodicity FROM habits WHERE name = ?', (name,))
    periodicity = cur.fetchone()[0]
    conn.execute('INSERT INTO habits (name, date, periodicity) VALUES (?, ?, ?)', (name, date, periodicity))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/analysis', methods=('GET', 'POST'))
def analysis():
   # app.config['DATABASE']  = 'habit_tracker.db'
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name FROM habits')
    habits = cur.fetchall()
    habits_ls = [element[0] for element in habits]
    most_habit = ''
    single_habits_set = set(habits_ls)
    show_habits = [i for i in single_habits_set]
    for habit in single_habits_set: 
        if habits_ls.count(habit) > habits_ls.count(most_habit):
            most_habit = habit
        elif habits_ls.count(habit) == habits_ls.count(most_habit):
            most_habit = habit, most_habit
    longest_streak = []
    conn = get_db_connection()
    cur = conn.cursor()
    #cur.execute('SELECT * FROM habits WHERE streak = (SELECT MAX(streak) FROM habits)')
    cur.execute('SELECT name FROM habits WHERE periodicity = ?', ('daily',))
    ls_daily = cur.fetchall()
    ls_daily_readable_set = set([i[0] for i in ls_daily])
    for i in ls_daily_readable_set:
        longest_streak.append([i, current_streak(i)[0]])

    all_dates = [i[1] for i in longest_streak]
    streak_count = max(all_dates)
    longest_habit_s = []
    for habit, date in longest_streak:
        if date == streak_count:
            longest_habit_s.append(habit) 

    cur = conn.cursor()
    cur.execute('SELECT name FROM habits WHERE periodicity = ?', ('daily',))
    dailies = set(cur.fetchall())
    cur = conn.cursor()
    cur.execute('SELECT name FROM habits WHERE periodicity = ?', ('weekly',))
    weeklies = set(cur.fetchall())
    
    cur.execute('SELECT name, periodicity FROM habits')
    all_habits = [i[0] for i in set(cur.fetchall())]
    conn.close()
    return render_template('analysis.html', variable_most_habit=most_habit, habits = show_habits, longest_streak_habit = longest_habit_s[0], longest_streak_streak = streak_count, daily_habits = dailies, weekly_habits = weeklies, all_habits = all_habits)  

@app.route('/submit-dropdown-analysis', methods = ('POST', 'GET'))
def analyze_selected():
    habit = request.form['dropdown']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT date FROM habits WHERE name = ?', (habit,))
    all_dates = cur.fetchall()
    r_all_dates = sorted([i[0] for i in all_dates])
    streak = current_streak(habit)
    return render_template('analysis_single.html', habit = habit, start_streak = streak[1][-1], end_streak = streak[1][0], habits = r_all_dates, streak = streak[0])

@app.route('/delete', methods=('POST', 'GET'))
def delete():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, date FROM habits ORDER BY id DESC')
    deletables = cur.fetchall()
    delete_choices = [{"id": item[0], "name": item[1], "date": item[2]} for item in deletables]
    cur.execute('SELECT name FROM habits')
    options1 = cur.fetchall()
    return render_template('delete.html', options=delete_choices, options1=set(options1))

@app.route('/delete_one', methods=('POST', 'GET'))
def delete_one():
    occurence_id = request.form['dropdown']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM habits WHERE id=?', (occurence_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete_all', methods=('GET', 'POST'))
def delete_all():
    name = request.form['dropdown']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM habits WHERE name=?', (name,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug= True)