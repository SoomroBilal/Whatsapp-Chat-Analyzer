import pandas as pd
import re
def preprocessor(data):
    # Pattern for reading date from a string
    pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"

    # Splitting string into date and message
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'User Messages': messages, 'Date': dates})

    # checking for date format
    if pd.to_datetime(df['Date'], format='%d/%m/%Y, %H:%M - ', errors='coerce').notnull().all():
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y, %H:%M - ')
    else:
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y, %H:%M - ')

    # Extracting names and messages from messages column
    users = []
    messages = []
    for message in df['User Messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group notification')
            messages.append(entry[0])

    df['Users'] = users
    df['messages'] = messages
    df.drop(columns=['User Messages'], inplace=True)
    df = df[df['Users'] != 'group notification']

    # creating separate columns for year, month, day, hour, minute  from date and time
    df['year'] = df['Date'].dt.year
    df['month'] = df['Date'].dt.month
    df['month_name'] = df['Date'].dt.month_name()
    df['day'] = df['Date'].dt.day
    df['day_name'] = df['Date'].dt.day_name()
    df['hour'] = df['Date'].dt.hour
    df['minute'] = df['Date'].dt.minute

    # Dividing time into periods like 0-1, 1-2, 2-3 etc
    period = []
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour)+ '-' + str(00))
        elif hour == 0:
            period.append(str(00) + "-" + str(hour+1))
        else:
            period.append(str(hour)+ "-" + str(hour+1))
    df['period'] = period

    return df
