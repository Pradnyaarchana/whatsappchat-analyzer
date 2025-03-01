from tenacity import retry_if_exception_type
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
extractor = URLExtract()



def fetch_ststs(selected_user, df):

    if selected_user != 'All':
        df= df[df['user'] == selected_user]
    # 1. no of messages
    num_messages =  df.shape[0]
    # no of words
    words = []
    for message in df['message']:

        words.extend(message.split())

    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    num_links = len(links)
    return num_messages, len(words), num_media, num_links


def most_busy_user(df):
    busy_users = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'user' :'Name', 'count':'Percent'})
    return busy_users, df


def create_wordcloud(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read().splitlines()  # Read stop words as a list

    f = open('stop_marathi.txt', 'r')
    stop_words_marathi = f.read().splitlines()

    if selected_user != 'All':
        df = df[df['user'] == selected_user]

    filtered_df = df[df['user'] != 'group notification']
    filtered_df = filtered_df[
        (filtered_df['message'] != '<Media omitted>\n') &
        (filtered_df['message'] != 'null') &
        (filtered_df['message'] != 'You deleted this message\n')
        ]
    filtered_df['message'] = filtered_df['message'].str.replace("<This message was edited>\n", "", regex=False)

    # Corrected function: It now takes a message as input
    def remove_stop_words(message):
        words = [word for word in message.lower().split() if word not in stop_words and word not in stop_words_marathi]
        return " ".join(words)

    # Apply the corrected function
    filtered_df['message'] = filtered_df['message'].apply(remove_stop_words)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(filtered_df["message"].str.cat(sep=' '))

    return df_wc


def most_common_words(selected_user , df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    f = open('stop_marathi.txt', 'r')
    stop_words_marathi = f.read()
    if selected_user != 'All':
        df= df[df['user'] == selected_user]

    filtered_df = df[df['user'] != 'group notification']
    filtered_df = filtered_df[(filtered_df['message'] != '<Media omitted>\n') & (filtered_df['message'] != 'null') & (filtered_df['message'] != 'You deleted this message\n')]
    filtered_df['message'] = filtered_df['message'].str.replace("<This message was edited>\n", "", regex=False)

    words = []
    for message in filtered_df['message']:
        for word in message.lower().split():
            if word not in stop_words and word not in stop_words_marathi:
                words.append(word)

    return pd.DataFrame(Counter(words).most_common(40))


def emoji_helper(selected_user, df):
    if selected_user != 'All':
        df= df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df