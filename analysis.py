import datetime
from database import get_db_connection
from flask import current_app


'''
requirements:
-
return a list of all currently tracked habits, check
-
return a list of all habits with the same periodicity,
-
return the longest run streak of all defined habits,
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
    '''
    year_data = all_dates_in_year(year)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name, date FROM habits WHERE name = ? ORDER BY date', (habit_name,))
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
    '''
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute('SELECT date FROM habits WHERE name = ? ORDER BY date', (habit_name,))
        data = cur.fetchall()
        
        if not data:
            return 0  # No data for the given habit_name
        
        readable_dates = sorted(list(set([item[0] for item in data])))
        streak = 0
        current_date = datetime.date.today()
        current_streak_date = current_date.strftime('%Y-%m-%d')
        
        # Check the current streak
        for i in range(len(readable_dates) - 1, -1, -1):
            if readable_dates[i] == current_streak_date:
                streak += 1
                current_date -= datetime.timedelta(days=1)
                current_streak_date = current_date.strftime('%Y-%m-%d')
            else:
                break
                
        return streak
    finally:
        pass
        #conn.close()

def maximum_streak(year, habit_name):
    year_data = all_dates_in_year(year)  # Generate a list of all dates in the given year
    conn = get_db_connection()  # Get a database connection
    cur = conn.cursor()  # Create a cursor object to interact with the database
    
    try:
        cur.execute('SELECT date FROM habits WHERE name = ?', (habit_name,))  # Fetch all dates for the given habit
        data = cur.fetchall()  # Retrieve all results from the query
        
        if not data:
            return 0  # If there are no records, return 0 as there are no streaks
        
        readable_dates = set([item[0] for item in data])  # Convert the dates to a set for efficient lookup
        streak = 0  # Initialize the current streak counter
        max_streak = 0  # Initialize the maximum streak counter
        
        for date in year_data:  # Iterate through all dates in the year
            if date in readable_dates:  # Check if the current date is in the set of habit dates
                streak += 1  # If it is, increment the current streak counter
                max_streak = max(max_streak, streak)  # Update the maximum streak if the current streak is higher
            else:
                streak = 0  # If the current date is not in the set, reset the current streak counter to 0
                
        return max_streak  # Return the maximum streak found
    finally:
        pass
        #conn.close()  # Ensure the database connection is closed after the operation
