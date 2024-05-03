import datetime
x = datetime.date.today
ls = [('awesomeness','2022-01-01'),('awesomeness', '2022-01-02'), ('awesomeness', '2022-01-03')]


def all_dates_in_year(year):
    start_date = datetime.date(year, 1, 1)  # First day of the year
    end_date = datetime.date(year, 12, 31)  
    delta = datetime.timedelta(days = 1) 

    ls_all_dates= [(start_date + i * delta).strftime('%Y-%m-%d') for i in range((end_date - start_date).days + 1)]
    return ls_all_dates
#print(all_dates_in_year(2024))

def streak_analysis(habit, year, date='2022-01-02'):
    print(f'0:{date}')
    year_data = all_dates_in_year(year)
    print(f'0.5:{year_data[0]}')
    habit_names = [item[0] for item in ls]
    print(f'1:{habit_names}')
    habit_dates = [item[1] for item in ls] 
    print(f'2:{habit_dates}')
    streak = 1
    test = date in year_data
    date_index_to_val = year_data.index(date)
    print(f'2.5: {test}')
    if habit in habit_names:
        print(f'3:habit was found')
        if date in year_data:
            print(f'4:date was found')
            print(f'4.5: {year_data.index(date)} date was found at this index.')
            for i in habit_dates:
                print('this habit already exists and has been recorded this year')
                if habit_dates[date_index_to_val] and date_index_to_val >= 1:
                    streak +=1
                    date_index_to_val -= 1
                    print(f'5: {date_index_to_val}')
    return print(f'analysis finished: streak = {streak}')

streak_analysis('awesomeness', 2022)

