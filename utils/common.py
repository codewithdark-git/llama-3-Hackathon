import streamlit as st
from utils.helper import fetch_articles, fetch_videos
from app import local_css

local_css("pages/style.css")

def articles_show(query):
    articles = fetch_articles(query)
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


def video_show(query):
    videos = fetch_videos(query)
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