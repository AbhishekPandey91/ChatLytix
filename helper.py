import pandas as pd

from  urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
# import emoji






extract = URLExtract()
def fetch_stats(selected_user,df):
    if selected_user != 'Full Analysis':
        df = df[df['user_name'] == selected_user]

    # getting the no.of messages
    num_messages = df.shape[0]

    # getting the total no. of words
    words =[]
    for message in df['msg']:
        words.extend(message.split())

    # getting the no. of media messages
    num_media_msg = df[df['msg']=='<Media omitted>'].shape[0]

    # getting no.of links shared
    links=[]
    for m  in df['msg']:
        links.extend(extract.find_urls(m))


    return num_messages,len(words) , num_media_msg , len(links)



## getting the most busy user

def most_busy_users(df):
    x = df['user_name'].value_counts().head()
    df1 = round((df['user_name'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'count':"percentage" , 'user_name':'user_name'})
    return x , df1


def create_wordcloud(selected_user,  df):

    f=open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Full Analysis':
        df = df[df['user_name'] == selected_user]

    temp=df[df['user_name'] != 'grp_notification']
    temp=temp[temp['msg'] != '<Media omitted>']

    def remove_stop_words(message):
        list1=[]
        for w in message.lower().split():
            if w not in stop_words:
                list1.append(w)
        return ' '.join(list1)


    wc = WordCloud(width=500, height=500,min_font_size=10, background_color='white')
    temp['msg']=temp['msg'].apply(remove_stop_words)
    df_wc = wc.generate(temp['msg'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user , df):

    f=open('stop_hinglish.txt','r')
    stop_words = f.read()
    if selected_user != 'Full Analysis':
        df = df[df['user_name'] == selected_user]
    temp = df[df['msg']!='grp_notification']
    temp = temp[temp['msg']!='<Media omitted>']

    words=[]
    for m in temp['msg']:
        for w in m.lower().split():
            if w not in stop_words:
                words.append(w)

    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

# def emoji_analysis(selected_user , df):
#     if selected_user != 'Full Analysis':
#         df = df[df['user_name'] == selected_user]

#     emojis=[]
#     for m in df['msg']:
#         emojis.extend([c for c in m if c in emoji.EMOJI_DATA])

#     emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
#     return emoji_df


def monthly_timeline(selected_user , df):
    if selected_user != 'Full Analysis':
        df = df[df['user_name'] == selected_user]

    timeline = df.groupby(['year','month_num','month_name']).count()['msg'].reset_index()

    time=[]
    for i in range (timeline.shape[0]):
        time.append(timeline['month_name'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline

def daily_timeline(selected_user , df):
    if selected_user != 'Full Analysis':
        df = df[df['user_name'] == selected_user]

    daily_timeline1 = df.groupby('only_date').count()['msg'].reset_index()

    return daily_timeline1


def week_activity_mapping(selected_user , df):
    if selected_user != 'Full Analysis':
        df = df[df['user_name'] == selected_user]
    return df['day_name'].value_counts()


def month_activity_mapping(selected_user , df):
    if selected_user != 'Full Analysis':
        df = df[df['user_name'] == selected_user]
    return df['month_name'].value_counts()


def activity_heatmap (selected_user , df):
    if selected_user != 'Full Analysis':
        df = df[df['user_name'] == selected_user]
    activity_heat = df.pivot_table(index='day_name', columns='period', values='msg', aggfunc='count').fillna(0)

    return activity_heat
