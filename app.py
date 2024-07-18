import streamlit as st
import asyncio
from youtubesearchpython import VideosSearch
import urllib.parse
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
        search_results = search(query, advanced=True, num_results=5)  # Store results
        for result in search_results:  # Iterate over results
            parsed_url = urllib.parse.urlparse(result.url)
            domain = parsed_url.netloc
            articles.append({
                'url': result.url,
                'title': result.title,
                'description': result.description,
                'domain': domain
            })  # Store all info for each article

    except Exception as e:
        print(f"Error fetching articles: {str(e)}")
    return articles



# Function to fetch YouTube videos
def fetch_youtube_videos(query):
    videos_search = VideosSearch(query, limit=6)
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
query = st.chat_input("Ask me anything...", key="user_query")


if query:
        st.markdown(f'##### {query}')
        with st.spinner("Researching and analyzing..."):

            response_text = asyncio.run(generate_response(query))
            # Fetch articles
            articles = fetch_articles(query)
            print(type(articles))

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
                                    <div class="source-title">{(article['title'][:100] if len(article['title']) > 50 else article['description'][:100])}</div>
                                    <div class="source-info">{article['domain'].removeprefix('www.')}</div>     
                                </a>
                                """, unsafe_allow_html=True)

            # Fetch and display YouTube videos
            videos = fetch_youtube_videos(query)
            with st.expander('Video Sources'):
                st.markdown("### Videos")
                row1 = st.columns(3)
                row2 = st.columns(3)
                rows = row1 + row2
                for i, video in enumerate(videos[:6]):
                    col = rows[i]
                    col.markdown(f"""
                                <div class="video-item">
                                            <a href="{video['link']}" target="_blank">
                                                <img src="{video['thumbnails'][0]['url']}" alt="{video['title']}" class="video-thumbnail">
                                                <p class="video-title">{video['title'][:50]}...</p>
                                                <div class="video-info">{video['channel']['name']}<br>
                                                {video['viewCount']['short']}
                                                </div>
                                            </a>
                                        </div>
                                        """, unsafe_allow_html=True)

            st.markdown("### Answer")
            st.write(response_text)

