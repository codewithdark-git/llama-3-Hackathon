import streamlit as st
from utils.llm import generate_response, generate_prompt
from utils.common import articles_show, video_show
from utils.helper import fetch_articles, fetch_videos
from utils.model import init_db, add_history
from app import local_css


# Initialize the database
init_db()
local_css("pages/style.css")

st.page_link('app.py', label='Back To Home', icon="🏠")
st.page_link('pages/history.py', label='See the History', icon="🕒")

query = st.chat_input("Ask me anything...", key="user_query")
if query:
        st.markdown(f'##### {query}')
        with st.spinner("Researching and analyzing..."):
            prompt = generate_prompt(query)
            response_text = generate_response(prompt)

            articles = fetch_articles(query)
            video = fetch_videos(query)

            add_history(query, response_text, articles, video)

            # Fetch and display articles
            with st.expander('Sources'):
                articles_show(query)

            # Fetch and display YouTube videos
            with st.expander('Video Sources'):
                video_show(query)

            st.markdown("### Answer")
            st.write(response_text)

