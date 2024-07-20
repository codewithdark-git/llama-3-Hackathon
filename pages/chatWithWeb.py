import streamlit as st
from utils.llm import generate_response, generate_prompt
from utils.common import articles_show, video_show
from app import local_css


# Function to generate related queries
async def generate_related_queries(query):
    prompt = f"Generate 3 related search queries for the following query: '{query}'. Provide only the queries, separated by newlines."
    response = await generate_response(prompt)
    return response.strip().split('\n')

local_css("pages/style.css")

st.page_link('app.py', label='Home', icon="🏠")
query = st.chat_input("Ask me anything...", key="user_query")
if query:
        st.markdown(f'##### {query}')
        with st.spinner("Researching and analyzing..."):
            prompt = generate_prompt(query)
            response_text = generate_response(prompt)

            # Fetch and display articles
            with st.expander('Sources'):
                articles_show(query)

            # Fetch and display YouTube videos
            with st.expander('Video Sources'):
                video_show(query)

            st.markdown("### Answer")
            st.write(response_text)

