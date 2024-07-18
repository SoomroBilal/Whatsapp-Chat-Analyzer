import streamlit as st
import preprocess, helper
import matplotlib.pyplot as plt
import seaborn as sns

# Sidebar
st.sidebar.title("Whatsapp Chat Analyzer")

# File Uploading
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess.preprocessor(data)
    st.dataframe(df)

    # Extracting Users
    user_list = df['Users'].unique().tolist()
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox("Show Analysis wrt: ", user_list)
    if st.sidebar.button("Show Analysis"):
        num_messages, num_words, num_media, num_url = helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)

        # Total messages
        with col1:
            st.header("Total messages")
            st.title(num_messages)

        # Total words
        with col2:
            st.header("Total words")
            st.title(num_words)

        # Media Shared
        with col3:
            st.header("Total media shared")
            st.title(num_media)

        # Urls Shared
        with col4:
            st.header("Total URLs shared")
            st.title(num_url)

        # Creating a line plot to show trend
        timeline = helper.monthly_timeline(df, selected_user)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['messages'])
        plt.ylabel("Number of Messages")
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        st.title("Activity map")
        col1, col2 = st.columns(2)

        # Showing the most busy days of the week
        with col1:
            st.header('Most busy day')
            busy_day = helper.week_activity_map(df, selected_user)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.ylabel("Number of Messages")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Most busy months
        with col2:
            st.header('Most busy month')
            busy_month = helper.monthly_activity_map(df, selected_user)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            plt.ylabel("Number of Messages")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Heatmap Shows time period with intensity of messages in it
        st.title("Weekly activity map")
        user_heatmap = helper.activity_heatmap(df, selected_user)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # Most Active users
        if selected_user == 'Overall':
            st.title('Most Busy users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            # Bar chart showing the users with their contribution
            with col1:
                ax.bar(x.index, x.values, color = 'red')
                plt.xticks(rotation='vertical')
                plt.ylabel("Number of Messages")
                st.pyplot(fig)

            # Showing all the users with their contribution percentage
            with col2:
                st.dataframe(new_df)

        # Word Cloud
        st.title("Most common words spoken")
        df_wc = helper.creat_worldcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Emojis Shared
        st.title("Most common emojis shared")
        emoji_df = helper.emoji_shared(df, selected_user)
        st.dataframe(emoji_df)




