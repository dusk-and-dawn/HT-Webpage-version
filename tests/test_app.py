import pytest
from app import app, init_db
import os
import sqlite3
from datetime import datetime
from database import get_db_connection
from flask import current_app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['DATABASE'] = 'test_habit_tracker.db'
    with app.app_context():
        init_db()
    with app.test_client() as client:
        yield client 
    os.remove(app.config['DATABASE'])  # Clean up the test database file

def test_db_init():
    # To protect the main database from interference with test data, a separate database (and app instance) just for testing is created
    app.config['DATABASE']  = 'test_habit_tracker.db'
    
    # Ensure the test database is clean before running the test
    if os.path.exists(app.config['DATABASE']):
        os.remove(app.config['DATABASE'])

    # Initialize the database
    with app.app_context():
        init_db()
 
    # Here come the actual tests: 
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute('''
        SELECT name FROM sqlite_master WHERE type='table';
    ''')
    table_check = cur.fetchone()
    assert table_check, 'Error: main table could not be created in Test data base'

    # as always, close db connection in the end
    conn.close()


def test_add_func(client):
    response = client.post('/add', data={'name':'test_habit_1'})
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute('''
        SELECT name, date, streak FROM habits;
    ''')
    add_check = cur.fetchall()
    print(f'add_check: {add_check}')
    name_check_readable = [item[0] for item in add_check]
    date_check_readable = [item[1] for item in add_check]
    streak_check_readable = [item[2] for item in add_check]
    print(f'name_check_readable: {name_check_readable}')
    print(f'date_check_readable: {date_check_readable}')
    print(f'streak_check_readable: {streak_check_readable}')

    date_local = str(datetime.now().date())
    assert response.status_code==302, 'Error: expected redirect after adding habit, but did not get a redirect'
    assert len(add_check) > 0, 'Error: could not add habit'
    assert name_check_readable[0] == 'test_habit_1', 'Error: test name not correct or not existing'
    assert date_check_readable[0] == date_local, 'Error: date logic in trouble'
    assert streak_check_readable[0] == 1, 'Error: check streak logic'
    conn.close()

def test_increment_func(client):
    with app.app_context():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO habits (name, date, streak) VALUES (?, ?, ?)',('test_habit', '2020-01-01', 1))
    response = client.get('/increment')

    assert response.status_code == 200
    assert 'Increment habit' in response.data.decode(), 'Error: Expected text "Increment habit" not found in response'

