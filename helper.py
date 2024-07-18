import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji

# Function for fetching stats
def fetch_stats(selected_user, df):
    if selected_user == 'Overall':
        num_messages = df.shape[0]
        words = []
        for message in df['messages']:
            words.extend(message.split())
        num_media = df[df['messages'] == '<Media omitted>\n'].shape[0]
        urls = []
        extractor = URLExtract()
        for message in df['messages']:
            urls.extend(extractor.find_urls(message))
        return num_messages, len(words), num_media, len(urls)
    else:
         new_df = df[df['Users'] == selected_user]
         num_messages = new_df.shape[0]
         words = []
         for message in new_df['messages']:
             words.extend(message.split())
         num_media = new_df[new_df['messages'] == '<Media omitted>\n'].shape[0]
         urls = []
         extractor = URLExtract()
         for message in new_df['messages']:
             urls.extend(extractor.find_urls(message))
         return num_messages, len(words), num_media, len(urls)

# Function for Calculating users' contribution
def most_busy_users(df):
    x = df['Users'].value_counts().head()
    df = round((df['Users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'Users':'Name','count':'Messages Percentage(%)'})
    df.index = df.index + 1
    return x, df

# Function for creating Wordcloud
def creat_worldcloud(selected_user, df):
    if selected_user!='Overall':
        df = df[df['Users']==selected_user]
    df = df[df['messages']!='<Media omitted>\n']
    df = df[df['messages'] != 'null\n']
    df = df[df['messages'] != 'Missed voice call\n']
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['messages'].str.cat(sep=" "))
    return df_wc

# Function for timeline
def monthly_timeline(df, selected_user):
    if selected_user!='Overall':
        df = df[df['Users']==selected_user]
    timeline = df.groupby(['year', 'month', 'month_name']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month_name'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

# Function for fetching busy days
def week_activity_map(df, selected_user):
    if selected_user!='Overall':
        df = df[df['Users']==selected_user]
    return df['day_name'].value_counts()

# Function for fetching busy months
def monthly_activity_map(df, selected_user):
    if selected_user!='Overall':
        df = df[df['Users']==selected_user]
    return df['month_name'].value_counts()

# Function for creating heatmap
def activity_heatmap(df, selected_user):
    if selected_user!='Overall':
        df = df[df['Users']==selected_user]

    user_heatmap = df.pivot_table(index = 'day_name', columns = 'period', values = 'messages', aggfunc='count').fillna(0)

    return user_heatmap

# Function for counting emojis
def emoji_shared(df, selected_user):
    if selected_user!='Overall':
        df = df[df['Users']==selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emoji_df.index = emoji_df.index + 1
    emoji_df = emoji_df.rename(columns={0:'Emoji', 1:'Counts'})
    return emoji_df
