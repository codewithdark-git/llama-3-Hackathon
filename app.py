import streamlit as st
import asyncio
from youtubesearchpython import VideosSearch
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import random
import time
from googlesearch import search
from g4f.client import AsyncClient
import g4f
from g4f.Provider.MetaAI import MetaAI


# Asynchronous function to generate AI response
async def generate_response(prompt):
    client = AsyncClient()
    try:
        response = await client.chat.completions.create(
            model=g4f.models.llama3_70b_instruct,
            messages=[{'role': 'user', 'content': prompt}],
            provider=MetaAI
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return None


# Function to fetch articles
def fetch_articles(query):
    articles = []
    try:
        for i, url in enumerate(search(query, stop=5), start=1):
            time.sleep(random.uniform(1, 3))
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            html = urlopen(req)
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.title.text if soup.title else "Title not found"
            domain = url.split("//")[-1].split("/")[0]
            articles.append({
                'url': url,
                'title': title,
                'source': domain,
                'number': i
            })
    except Exception as e:
        print(f"Error fetching articles: {str(e)}")
    return articles


# Function to fetch YouTube videos
def fetch_youtube_videos(query):
    videos_search = VideosSearch(query, limit=4)
    return videos_search.result()['result']


# Function to generate related queries
async def generate_related_queries(query):
    prompt = f"Generate 3 related search queries for the following query: '{query}'. Provide only the queries, separated by newlines."
    response = await generate_response(prompt)
    return response.strip().split('\n')


# Streamlit app
st.set_page_config(page_title="AI Research Assistant")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style.css")

# Main layout
st.title("AI Research Assistant")

# Create two columns for the main layout
col1, col2 = st.columns([2, 1], gap='small', vertical_alignment="top")
query = st.chat_input("Ask me anything...", key="user_query")


if query:
        st.markdown(f'##### {query}')
        with st.spinner("Researching and analyzing..."):

                response_text = asyncio.run(generate_response(query))
                # Fetch articles
                articles = fetch_articles(query)

                # Display AI respo
                # Display sources
                with st.expander('Sources'):

                    # Create two rows of columns
                    st.markdown("### Sources")
                    row1 = st.columns(3)
                    row2 = st.columns(3)
                    rows = row1 + row2

                    for i, article in enumerate(articles[:6]):
                        col = rows[i]
                        col.markdown(f"""
                                <a href="{article['url']}" target="_blank" class='source-button'>
                                    <div class="source-title">{article['title'][:50]}</div>
                                    <div class="source-info">
                                        <span>{article['source']}</span>
                                    </div>
                                </a>
                                """, unsafe_allow_html=True)


                st.markdown("### Answer")
                st.write(response_text)


        # Fetch and display YouTube videos
        videos = fetch_youtube_videos(query)
        st.markdown("### Video Sources")
        for video in videos:
            st.markdown(f"""
            <div class="video-item">
                <a href="{video['link']}" target="_blank">
                    <img src="{video['thumbnails'][0]['url']}" alt="{video['title']}" class="video-thumbnail">
                </a>
            </div>
            """, unsafe_allow_html=True)
