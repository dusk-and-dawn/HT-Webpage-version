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
    names = ['test_habit_1', 'test_habit_2', 'test_habit_3']
    response = client.post('/add', data={'name':[i for i in names], 'periodicity':'daily'})
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute('''
        SELECT name, date, streak, periodicity FROM habits;
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
    conn.close()

def test_increment_func(client):
    with app.app_context():
        conn = get_db_connection()
        cur = conn.cursor()
        conn.execute('INSERT INTO habits (name, date, streak, periodicity) VALUES (?, ?, ?, ?)',('test_habit', '2020-01-01', 1, 'daily'))
        cur.execute('SELECT name, date FROM habits')
        test_data = [i[0] for i in cur.fetchall()]
    response = client.get('/increment')

    assert response.status_code == 200
    assert 'Increment habit' in response.data.decode(), 'Error: Expected text "Increment habit" not found in response'
    assert test_data[0] == 'test_habit', 'wrong name was found after increment func'


#verify shit below this line 

def test_increment_route(client):
    with app.app_context():
    # Insert test data into the test database
        conn = get_db_connection()
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit1', 2024-06-01, 'weekly')")
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit2',  2024-06-01,'daily')")
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit3',  2024-06-01,'weekly')")
        conn.commit()
        conn.close()

        # Send a GET request to the /increment route
    response = client.get('/increment')
    
    # Check that the response is 200 OK
    assert response.status_code == 200
    
    # Check that the response data contains the expected habit names
    assert b'habit1' in response.data
    assert b'habit2' in response.data
    assert b'habit3' in response.data

def test_submit_dropdown_route(client):
    with app.app_context():
    # Insert initial habit data into the test database
        conn = get_db_connection()
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit1', 2024-06-01, 'weekly')")
        conn.commit()
        conn.close()

        # Send a POST request to the /submit-dropdown route with form data
    response = client.post('/submit-dropdown', data={'dropdown': 'habit1'})

    # Check that the response is a redirect to the index page
    assert response.status_code == 302
    assert response.location.endswith('/')

    # Verify that the data was correctly inserted into the database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, date, periodicity FROM habits WHERE name = 'habit1' ORDER BY rowid DESC")
    result = cur.fetchone()
    assert result is not None
    assert result['name'] == 'habit1'
    assert result['date'] == datetime.now().date().strftime('%Y-%m-%d')
    assert result['periodicity'] == 'weekly'  # Ensures that the periodicity is correct
    conn.close()

def test_record_alternative_date_route(client):
    with app.app_context():
    # Insert initial habit data into the test database
        conn = get_db_connection()
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit1', '2024-06-01', 'daily')")
        conn.commit()
        conn.close()

        # Send a POST request to the /record-alternative-date route with form data
    response = client.post('/record-alternative-date', data={'dropdown': 'habit1', 'date': '2024-06-22'})

    # Check that the response is a redirect to the index page
    assert response.status_code == 302
    assert response.location.endswith('/')

    # Verify that the data was correctly inserted into the database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, date, periodicity FROM habits WHERE name = 'habit1' ORDER BY rowid DESC")
    result = cur.fetchone()
    assert result is not None
    assert result['name'] == 'habit1'
    assert result['date'] == '2024-06-22'
    assert result['periodicity'] == 'daily'  # Ensures that the periodicity is correct
    conn.close()


    #lets see how to test the analysis module 
def test_analysis_module(client):
    print('starting analysis test')
    with app.app_context():
    # Insert test data into the test database
        conn = get_db_connection()
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit1', '2024-06-01','daily')")
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit1', '2024-06-02','daily')")
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit1', '2024-06-03','daily')")
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit1', '2024-06-04','daily')")
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit1', '2024-06-05','daily')")
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit1', '2024-06-06','daily')")
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit1', '2024-06-07','daily')")
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit1', '2024-06-08','daily')")
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit1', '2024-06-09','daily')")
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit1', '2024-06-10','daily')")
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit1', '2024-06-11','daily')")
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit1', '2024-06-12','daily')")
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit1', '2024-06-13','daily')")
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit1', '2024-06-15','daily')") # this day should not be counted for the streak, hence streak should equal 13
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit2', '2024-06-01','daily')")
        conn.commit()
    
        cur = conn.cursor()
        cur.execute('SELECT name, date, periodicity FROM habits WHERE name == ?', ('habit1',))
        readable = [i[:] for i in cur.fetchall()]
        print(readable)
        
        conn.close()  

    response = client.get('/analysis')   
    assert response.status_code == 200, 'could not access analysis module'
    data = response.data.decode('utf-8')
    #print(data) this can be displayed by adding -s to the test call 
    assert 'habit1' in data, 'problem with the streak analysis'
    assert 'habit2' in data, 'second habit missing - analysis problematic'
    assert 'Your longest streak was of the habit: habit1 which you recorded for 13 units.', 'expected streak to be 13 units long' #test of the streak 
  