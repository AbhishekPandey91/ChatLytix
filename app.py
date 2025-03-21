import streamlit as st
import matplotlib.pyplot as plt
import helper
import preprocessor
import seaborn as sns


# Add a sleek header with a modern gradient
def add_header():
    st.markdown(
        """
        <style>
        .header {
            padding: 12px 0;
            width: 100%;
            text-align: center;
            background: linear-gradient(90deg, #1F1C2C, #928DAB);
            color: white;
            font-size: 26px;
            font-weight: bold;
            margin-top: 20px; /* Fixed the margin */
            margin-bottom:20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }
        .main .block-container {
            padding-top: 20px; /* Added some padding to avoid overlap */
        }
        </style>
        <div class="header">
            🚀 ChatLytix - Analyze Group & Personal Chats Easily 📊
        </div>
        """,
        unsafe_allow_html=True
    )

# Call the header function at the start
add_header()



st.title("Get Smart with Numbers🧩—Meet ChatLytix!👾" )
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocesss(data)
    st.title("All Chats in a DataFrame")
    st.dataframe(df)

    # finding unique user_name

    list_user=df['user_name'].unique().tolist()
    list_user.remove("grp_notification")
    list_user.sort()
    list_user.insert(0,"Full Analysis")

    selected_user = st.sidebar.selectbox("Give Analysis",list_user)

    if st.sidebar.button("Give Analysis"):

        num_msgs , words , num_media_msg  , num_links= helper.fetch_stats(selected_user,df)
        st.title('Top Statistics')
        col1 , col2 , col3 , col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_msgs)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media Shared")
            st.title(num_media_msg)
        with col4:
            st.header("Total Links")
            st.title(num_links)

        ###  MONTHLY TIMELINE
        timeline=helper.monthly_timeline(selected_user,df)
        fig , ax = plt.subplots()
        st.title("Monthly Timeline")
        ax.plot(timeline['time'] ,timeline['msg'])
        plt.xticks(rotation=90)
        st.pyplot(fig)


        ### DAILY TIMELINE

        daily_timeline1 = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        st.title("Daily Timeline")
        ax.plot(daily_timeline1['only_date'], daily_timeline1['msg'] , color='purple')
        plt.xticks(rotation=90)
        st.pyplot(fig)


        ### ACTIVITY MAPPING
        st.title("Activity Map")
        col1,col2=st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_mapping(selected_user, df)
            fig , ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation=90)
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_mapping(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values , color='orange')
            plt.xticks(rotation=90)
            st.pyplot(fig)


        st.title("Weekly Activity HeatMap")
        activity_heat = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(activity_heat)
        st.pyplot(fig)


        ### FINDING THE BUSIEST USer in group (only for group level)
        if selected_user == "Full Analysis":
            st.title("The most Busy User")
            x , df1 =helper.most_busy_users(df)
            fig,ax = plt.subplots()
            col1, col2  = st.columns(2)

            with col1:
                ax.bar(x.index, x.values , color="green")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(df1)

        ## WORDCLOUD
        st.title("WordCloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig , ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        ## MOST COMMON WORDS

        most_common_df= helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()
        ax.barh(most_common_df[0] , most_common_df[1])
        st.title("Most Common Words")
        st.pyplot(fig)

        ## EMOJI ANALYSIS
        # emoji_df = helper.emoji_analysis(selected_user , df )
        # st.title("Emoji Analysis")

        # # col1, col2 = st.columns(2)
        # # with col1:
        # st.dataframe(emoji_df)
        # with col2:
        #     fig,ax = plt.subplots()
        #     ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct='%0.2f')
        #     st.pyplot(fig)


import streamlit as st

# Add footer
def add_footer():
    footer = """
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f1f1f1;
            color: #333;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            border-top: 1px solid #ddd;
        }
        .footer a {
            color: #0073b1;  /* LinkedIn Blue */
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
    </style>
    <div class="footer">
        © 2025 <b>ChatLytix</b>. All rights reserved. |
        Contact: <a href="mailto:pandeyabhishek8685@gmail.com">pandeyabhishek8685@gmail.com</a> |
        <a href="https://www.linkedin.com/in/pandeyabhishek25" target="_blank">LinkedIn</a>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)

# Call the footer function at the end
add_footer()










