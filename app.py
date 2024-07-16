import streamlit as st
import requests
from bs4 import BeautifulSoup
from youtubesearchpython import Search
from g4f.client import Client
import g4f
from g4f.Provider.MetaAI import MetaAI
from urllib.request import urlopen
from googlesearch import search


# Function to generate AI response
def generate_response(prompt):
    client = Client()
    try:
        response = client.chat.completions.create(
            model=g4f.models.llama3_70b_instruct,
            messages=[{'role': 'user', 'content': prompt}],
            provider=MetaAI
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return None

# Function to validate URLs
def validate_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Function to fetch articles
def fetch_articles(query):
    articles = []
    try:
        for url in search(query, stop=5):  # Fetch top 5 articles
            html = urlopen(url)
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.title.text if soup.title else "Title not found"
            description = soup.find('meta', attrs={'name': 'description'})
            description_content = description["content"] if description else "Description not found"
            domain = url.split("//")[-1].split("/")[0]
            articles.append({'url': url, 'title': title, 'description': description_content, 'domain': domain})
    except Exception as e:
        st.error(f"Error fetching articles: {str(e)}")
    return articles

# Function to fetch YouTube videos
def fetch_youtube_videos(query):
    allSearch = Search(query, limit=5)
    videos = []
    for video in allSearch.result()['result']:
        videos.append({'title': video['title'], 'link': video['link']})
    return videos

# Function to generate prompts
def generate_prompt(query):
    prompt = f"""
        
        Based on the user's query "{query}", provide a concise but comprehensive overview of the topic. Your response should:
        1. Offer a brief introduction to the subject.
        2. Highlight key concepts or ideas related to the query.
        3. Mention any current trends or recent developments.
        4. If applicable, touch on different perspectives or debates surrounding the topic.

        Format your response as a short, well-structured paragraph.

        """
    return prompt

# Streamlit app
st.title("Enhanced AI Query Assistant")

query = st.chat_input("Enter your query:")

if query:
    with st.spinner("Searching for relevant content and generating expert analysis..."):
        articles = fetch_articles(query)
        videos = fetch_youtube_videos(query)
        in_depth_prompt = generate_prompt(query)
        response_text = generate_response(in_depth_prompt)

    if response_text:
        st.subheader("Answer")
        st.markdown(response_text)

        st.subheader("Sources")


        if videos:
            cols = st.columns(5)
            for idx, video in enumerate(videos):
                with cols[idx % 5]:
                    # st.markdown(f"[{video['title']}]({video['url']})")
                    st.video(video['link'])

        st.subheader("Related Questions")
        st.markdown("* Who is Leonard Nimoy, the actor behind Mr. Spock?")
        st.markdown("* What is the traditional Jewish blessing behind 'live long and prosper'?")
        st.markdown("* What is the Vulcan salute and how was it devised by Leonard Nimoy?")
    else:
        st.error("Unable to generate an analysis. Please try again or refine your query.")