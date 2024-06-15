from datetime import datetime, timedelta
from database import get_db_connection
from flask import current_app


'''
requirements:
-
return a list of all currently tracked habits, check
-
return a list of all habits with the same periodicity, check
-
return the longest run streak of all defined habits, check 
-
and return the longest run streak for a given habit.
'''
def all_dates_in_year(year):
    start_date = datetime.date(year, 1, 1)  # First day of the year
    end_date = datetime.date(year, 12, 31)  
    delta = datetime.timedelta(days = 1) 

    ls_all_dates= [(start_date + i * delta).strftime('%Y-%m-%d') for i in range((end_date - start_date).days + 1)]
    return ls_all_dates

def current_streak(habit_name): #prior name analysis_streak 
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT date FROM habits WHERE name = ? ORDER BY date', (habit_name,))
    data = cur.fetchall()
    
    if not data:
        return 0  # No data for the given habit_name
    
    readable_dates = sorted(list(set([item[0] for item in data])))
    streak = 0
    current_streak_date = readable_dates[-1]
    actual_streak_d = []
    # Check the current streak
    for i in range(len(readable_dates) - 1, -1, -1):
        if readable_dates[i] == current_streak_date:
            streak += 1
            actual_streak_d.append(readable_dates[i])
            transformer = datetime.strptime(current_streak_date, '%Y-%m-%d')
            transformer -= timedelta(days=1)
            current_streak_date = transformer.strftime('%Y-%m-%d')
        else:
            break
            
    return streak, actual_streak_d
