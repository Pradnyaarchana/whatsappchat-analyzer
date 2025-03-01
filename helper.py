from tenacity import retry_if_exception_type
from urlextract import URLExtract
from wordcloud import WordCloud
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
    if selected_user != 'All':
        df= df[df['user'] == selected_user]

    df["message"] = df["message"].str.replace(r'<Media omitted>\n', '', regex=True)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df["message"].str.cat(sep=' '))
    return df_wc

def most_common_words(selected_user , df):
    if selected_user != 'All':
        df= df[df['user'] == selected_user]

    filtered_df = df[df['user'] != 'group notification']
    filtered_df = filtered_df[filtered_df['message'] != '<Media omitted>\n']

    words = []
    for message in filtered_df['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
