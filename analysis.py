import datetime
from database import get_db_connection
from flask import current_app

def all_dates_in_year(year):
    start_date = datetime.date(year, 1, 1)  # First day of the year
    end_date = datetime.date(year, 12, 31)  
    delta = datetime.timedelta(days = 1) 

    ls_all_dates= [(start_date + i * delta).strftime('%Y-%m-%d') for i in range((end_date - start_date).days + 1)]
    return ls_all_dates

def analysis_streak(year, habit_name):
    year_data = all_dates_in_year(year)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name, date FROM habits WHERE name = ?', (habit_name,))
    data = cur.fetchall()
    readable_dates = set([item[1] for item in data])
    readable_name = data[0][0]
    streak = 1 
    for date in readable_dates: 
        if year_data[year_data.index(date)-1] in readable_dates:
            streak +=1
        else:
            pass
    return streak


