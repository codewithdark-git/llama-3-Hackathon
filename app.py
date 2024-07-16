import streamlit as st
import requests
from bs4 import BeautifulSoup
from youtubesearchpython import VideosSearch
from g4f.client import Client
import g4f
from urllib.parse import urlparse, urljoin

# Function to generate AI response
def generate_response(prompt):
    client = Client()
    try:
        response = client.chat.completions.create(
            model='llama3_70b_instruct',
            messages=[{'role': 'user', 'content': prompt}],
            provider=g4f.provider.MetaAI
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
    search_url = f"https://www.google.com/search?q={query}&tbm=nws"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []
    for item in soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd'):
        title = item.text
        link_element = item.find_parent('a')
        if link_element and 'href' in link_element.attrs:
            link = link_element['href'].replace('/url?q=', '')
            parsed_url = urlparse(link)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            full_url = urljoin(base_url, parsed_url.path)
            if validate_url(full_url):
                articles.append({'title': title, 'link': full_url})
    return articles[:5]  # Return only top 5 valid articles

# Function to fetch YouTube videos
def fetch_youtube_videos(query):
    videos_search = VideosSearch(query, limit=5)
    videos = []
    for video in videos_search.result()['result']:
        video_url = f"https://www.youtube.com/watch?v={video['id']}"
        if validate_url(video_url):
            videos.append({'title': video['title'], 'url': video_url})
    return videos

# Function to fetch web search results

# Function to generate prompts
def generate_prompt(query):
    prompt = f"""
        Based on the user's query "{query}", identify the 5 most relevant and informative webpages
        that address the user's intent. Prioritize content that is trustworthy, up-to-date,
        and well-written. For each webpage, provide:

        1. Title: A concise, descriptive title of the webpage.
        2. Summary: A brief, informative summary of the key points (2-3 sentences).
        3. Link: The full URL of the webpage.

        Ensure that each webpage entry follows this exact format:
        Title: [Webpage Title]
        Summary: [Brief summary of key points]
        Link: [Full URL]

        Focus on authoritative sources, recent publications, and comprehensive coverage of the topic.
        Avoid duplicates and ensure a diverse range of perspectives if applicable.
        """
    return prompt

# Streamlit app
st.title("Enhanced AI Query Assistant")

query = st.text_input("Enter your query:").capitalize()

if query:
    with st.spinner("Searching for relevant content and generating expert analysis..."):
        articles = fetch_articles(query)
        web_results = fetch_youtube_videos(query)
        web_search = articles, web_results
        in_depth_prompt = generate_prompt(query)
        response_text = generate_response(in_depth_prompt)

    if response_text:
        st.subheader("Expert AI Analysis:")
        st.markdown(response_text)

        if web_search:
            st.subheader("Relevant Web Sources")
            for result in web_results, articles:
                if web_search:
                    for item in web_search:
                        st.write(f"{item['title']}: {item['link']}")
                elif articles:
                    for item in articles:
                        st.write(f"{item['title']}: {item['link']}")

        else:
            st.info("No relevant web sources found. The analysis is based on the AI's general knowledge.")

        st.info("All listed sources have been verified for accessibility.")
    else:
        st.error("Unable to generate an analysis. Please try again or refine your query.")
