import re
import pandas as pd


def preprocesss(data):
    # First, determine the date format by checking the first few lines
    if re.search(r'\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\sPM|\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\sAM', data):
        # Format: M/DD/YY, H:MM AM/PM (US format)
        pattern = r'\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[APap][Mm]\s-\s'
        datetime_pattern = r"(\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[APap][Mm])\s-\s(.+)"
        date_format = '%m/%d/%y, %I:%M %p'
    else:
        # Format: DD/MM/YY, H:MM am/pm (non-US format)
        pattern = r'\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[ap]m\s-\s'
        datetime_pattern = r"(\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[ap]m)\s-\s(.+)"
        date_format = '%d/%m/%y, %I:%M %p'

    # Clean up any Unicode characters that might cause issues
    data = data.replace('\u202fam', 'am')
    data = data.replace('\u202fpm', 'pm')

    # Extract matches using the appropriate pattern
    matches = re.findall(datetime_pattern, data)

    # If no matches found, try alternative pattern (sometimes WhatsApp formats change)
    if not matches:
        # Try a more general pattern
        general_pattern = r"(\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2})\s-\s(.+)"
        matches = re.findall(general_pattern, data)
        date_format = '%d/%m/%y, %H:%M'  # Adjust format for 24-hour time

    # If still no matches, print diagnostic info and return empty DataFrame
    if not matches:
        print("No matches found in the data. First 200 characters of data:")
        print(data[:200])
        return pd.DataFrame(columns=['msg_dates', 'user_name', 'msg', 'only_date', 'year',
                                     'month_num', 'month_name', 'day', 'day_name', 'hour',
                                     'minute', 'period'])

    # Convert to DataFrame
    df = pd.DataFrame(matches, columns=['msg_dates', 'user_msg'])

    # Function to extract user_name and msg
    def split_message(text):
        try:
            match = re.match(r"^(.*?):\s(.+)$", text)
            if match:
                return match.group(1), match.group(2)  # Extract user_name and msg
            return "grp_notification", text  # If no match, mark as a group notification
        except:
            # Handle any unexpected errors and return a default
            return "unknown", text

    # Apply function to DataFrame and handle cases where split doesn't work
    try:
        series_result = df['user_msg'].apply(lambda x: pd.Series(split_message(x)))
        if len(series_result.columns) == 2:
            df[['user_name', 'msg']] = series_result
        else:
            # Handle case where split didn't work correctly
            df['user_name'] = 'unknown'
            df['msg'] = df['user_msg']
    except Exception as e:
        print(f"Error splitting messages: {e}")
        df['user_name'] = 'unknown'
        df['msg'] = df['user_msg']

    # Drop the original user_msg column
    df = df.drop(columns=['user_msg'])

    # Try to convert dates, handling potential format issues
    try:
        df['msg_dates'] = pd.to_datetime(df['msg_dates'], format=date_format)
    except ValueError:
        # Try alternative date formats if the first one fails
        try:
            # For US format
            df['msg_dates'] = pd.to_datetime(df['msg_dates'], format='%m/%d/%y, %I:%M %p')
        except ValueError:
            try:
                # For non-US format with 24-hour time
                df['msg_dates'] = pd.to_datetime(df['msg_dates'], format='%d/%m/%y, %H:%M')
            except ValueError:
                # Last resort: Let pandas infer the format
                df['msg_dates'] = pd.to_datetime(df['msg_dates'], errors='coerce')

    # Extract date components
    df['only_date'] = df['msg_dates'].dt.date
    df['year'] = df['msg_dates'].dt.year
    df['month_num'] = df['msg_dates'].dt.month
    df['month_name'] = df['msg_dates'].dt.month_name()
    df['day'] = df['msg_dates'].dt.day
    df['day_name'] = df['msg_dates'].dt.day_name()
    df['hour'] = df['msg_dates'].dt.hour
    df['minute'] = df['msg_dates'].dt.minute

    # Create period column
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
