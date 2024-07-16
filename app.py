import streamlit as st
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from youtubesearchpython import VideosSearch
from g4f.client import Client
import g4f

def generate_response(prompt):
    client = Client()
    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[{'role': 'user', 'content': prompt}],
        # provider=g4f.Provider.MetaAI
    )
    response = response.choices[0].message.content
    return response


def generate_prompt(query):
    # Customize this function to generate a professional prompt based on the user query
    prompt = f"""
Subject: In-depth Analysis Request on "{query}"

Dear Expert,

I hope this message finds you well. I am currently engaged in a comprehensive study pertaining. Your profound insights and expertise in this domain are highly esteemed, and I would be immensely grateful if you could provide a detailed analysis on the following aspects:

1. Historical Context and Evolution".
2. Current Trends and Market Dynamics.
3. Technological Advancements and Innovations.
4. Regulatory and Compliance Considerations.
5. Future Projections and Potential Challenges.

Please let me know if you require any further information or specific data points to facilitate your analysis. Your contribution will be invaluable to my research.

Thank you very much for your time and expertise.

"""
    return prompt



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
            link = link_element['href']
            articles.append({'title': title, 'link': link})
    return articles

# Function to fetch YouTube videos
def fetch_youtube_videos(query):
    videos_search = VideosSearch(query)
    videos = []
    for video in videos_search.result()['result']:
        videos.append({'title': video['title'], 'url': f"https://www.youtube.com/watch?v={video['id']}"})
    return videos


# Streamlit app
st.title("AI Query Assistant")
query = st.text_input("Enter your query:")

if query:
    response_text = generate_response(query)
    videos = fetch_youtube_videos(query)

    st.subheader("Response Text")
    st.write(response_text)

    st.subheader("Articles")
    articles = fetch_articles(query)
    for article in articles[:5]:
        st.write(article['title'])
        st.write(article['link'])

    st.subheader("Videos")
    for video in videos[:5]:
        st.write(video['title'])
        st.write(video['url'])

