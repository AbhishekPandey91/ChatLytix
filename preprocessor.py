import re



def preprocesss (data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)
    data = data.replace('\u202fam', '-')
    data = data.replace('\u202fpm', '-')
    datetime_pattern = r"\b\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}\b"
    dates = re.findall(datetime_pattern, data)
    pattern1 = r"(\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2})- - (.+)"

    # Extract matches
    matches = re.findall(pattern1, data)
    import pandas as pd

    # Convert to DataFrame
    df = pd.DataFrame(matches, columns=['msg_dates', 'user_msg'])

    # Regular expression to split user_name and msg
    pattern = r"^(.*?):\s(.+)$"
    # pattern = r"(\d{2}/\d{2}/\d{2,4}),\s(\d{1,2}:\d{2})\s?(am|pm|AM|PM| am| pm)?\s-\s(.+)"

    # Function to extract user_name and msg
    def split_message(text):
        match = re.match(pattern, text)
        if match:
            return match.group(1), match.group(2)  # Extract user_name and msg
        return "grp_notification", text  # If no match, mark as a group notification

    # Apply function to DataFrame
    df[['user_name', 'msg']] = df['user_msg'].apply(lambda x: pd.Series(split_message(x)))

    df = df.drop(columns=['user_msg'])

    import pandas as pd

    # Convert 'msg_dates' to datetime format
    df['msg_dates'] = pd.to_datetime(df['msg_dates'], format='%d/%m/%y, %H:%M')

    # Extract required columns
    df['only_date'] = df['msg_dates'].dt.date
    df['year'] = df['msg_dates'].dt.year
    df['month_num'] = df['msg_dates'].dt.month
    df['month_name'] = df['msg_dates'].dt.month_name()
    df['day'] = df['msg_dates'].dt.day
    df['day_name'] = df['msg_dates'].dt.day_name()
    df['hour'] = df['msg_dates'].dt.hour
    df['minute'] = df['msg_dates'].dt.minute

    period=[]
    for hour in df[['day_name','hour']]['hour']:
        if hour ==23:
            period.append(str(hour) +  "-"  + str('00'))
        elif hour ==0:
            period.append(str('00') + "-" + str(hour + 1))
        else :
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df


