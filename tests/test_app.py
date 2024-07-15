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
    os.remove(app.config['DATABASE'])  

def test_db_init():
    app.config['DATABASE']  = 'test_habit_tracker.db'
    
    if os.path.exists(app.config['DATABASE']):
        os.remove(app.config['DATABASE'])

    with app.app_context():
        init_db()
 
# *****************Here come the actual tests: *****************

    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute('''
        SELECT name FROM sqlite_master WHERE type='table';
    ''')
    table_check = cur.fetchone()
    assert table_check, 'Error: main table could not be created in Test data base'

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
    name_check_readable = [item[0] for item in add_check]
    date_check_readable = [item[1] for item in add_check]
    conn.close()
    date_local = str(datetime.now().date())
    assert response.status_code==302, 'Error: expected redirect after adding habit, but did not get a redirect'
    assert len(add_check) > 0, 'Error: could not add habit'
    assert name_check_readable[0] == 'test_habit_1', 'Error: test name not correct or not existing'
    assert date_check_readable[0] == date_local, 'Error: date logic in trouble'


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

def test_increment_route(client):
    with app.app_context():
        conn = get_db_connection()
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit1', 2024-06-01, 'weekly')")
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit2',  2024-06-01,'daily')")
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit3',  2024-06-01,'weekly')")
        conn.commit()
        conn.close()

    response = client.get('/increment')
    
    assert response.status_code == 200
    assert b'habit1' in response.data
    assert b'habit2' in response.data
    assert b'habit3' in response.data

def test_submit_dropdown_route(client):
    with app.app_context():
        conn = get_db_connection()
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit1', 2024-06-01, 'weekly')")
        conn.commit()
        conn.close()

    response = client.post('/submit-dropdown', data={'dropdown': 'habit1'})

    assert response.status_code == 302
    assert response.location.endswith('/')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, date, periodicity FROM habits WHERE name = 'habit1' ORDER BY rowid DESC")
    result = cur.fetchone()
    assert result is not None
    assert result['name'] == 'habit1'
    assert result['date'] == datetime.now().date().strftime('%Y-%m-%d')
    assert result['periodicity'] == 'weekly'  
    conn.close()

def test_record_alternative_date_route(client):
    with app.app_context():
        conn = get_db_connection()
        conn.execute("INSERT INTO habits (name, date, periodicity) VALUES ('habit1', '2024-06-01', 'daily')")
        conn.commit()
        conn.close()

    response = client.post('/record-alternative-date', data={'dropdown': 'habit1', 'date': '2024-06-22'})

    assert response.status_code == 302
    assert response.location.endswith('/')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, date, periodicity FROM habits WHERE name = 'habit1' ORDER BY rowid DESC")
    result = cur.fetchone()
    assert result is not None
    assert result['name'] == 'habit1'
    assert result['date'] == '2024-06-22'
    assert result['periodicity'] == 'daily'  
    conn.close()

def test_analysis_module(client):
    print('starting analysis test')
    with app.app_context():
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
    print(data) #this can be displayed by adding -s to the test call 
    assert 'habit1' in data, 'problem with the streak analysis'
    assert 'habit2' in data, 'second habit missing - analysis problematic'
    assert 'Your longest streak was of the habit: habit1 which you recorded for 13 units.' in data, 'expected streak to be 13 units long' #test of the streak 
