import re
import pandas as pd


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_messages': messages, 'date': dates})
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %H:%M - ')

    # seperate user and messages
    user = []
    message = []

    for messages in df['user_messages']:
        entry = re.split(r'([\w\W]+?):\s', messages)
        if entry[1:]:  # user_name
            user.append(entry[1])
            message.append(entry[2])
        else:
            user.append('group notification')
            message.append(entry[0])

    df['user'] = user
    df['message'] = message

    df.drop(columns=['user_messages'], inplace=True)

    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['year'] = df['date'].dt.year
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df