import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes(stream):
    bytes_data = uploaded_file.getvalue()
    # converting stream into text
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)
    st.dataframe(df)

    user_list = df['user'].unique().tolist()
    if 'group notification' in user_list:
        user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0,"All")
    selected_user = st.sidebar.selectbox("Select users", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media, num_links= helper.fetch_ststs(selected_user, df) #Total no of messages

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media shared")
            st.title(num_media)
        with col4:
            st.header("Links shared")
            st.title(num_links)

        # finding busiest users in the group
        if selected_user == 'All':
            st.title('Busiest Users')
            col1, col2 = st.columns(2)
            df_filtered = df[df['user'] != 'group notification']
            busy_users, busy_users_df = helper.most_busy_user(df_filtered)
            fig, ax = plt.subplots()
            name = busy_users.index
            count = busy_users.values

            with col1:
                ax.bar(name, count)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(busy_users_df)


        #wordcloud
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax  = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_cmn_df = helper.most_common_words(selected_user, df)
        st.dataframe(most_cmn_df)

        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")
        st.dataframe(emoji_df)
