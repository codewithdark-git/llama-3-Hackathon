import streamlit as st
import json
from utils.model import get_history
from app import local_css
from utils.common import articles_show, video_show
import sqlite3

# Apply custom CSS
local_css("pages/style.css")

st.page_link('app.py', label='Back To Home', icon="🏠")
st.page_link('pages/chatWithWeb.py', label='Back To Chat With Web', icon="🔙")
st.markdown("### Your Recent Chats")

def display_saved_notes(c, conn):
    c.execute("SELECT id, query, response, articles, videos, timestamp FROM history ORDER BY timestamp DESC")
    rows = c.fetchall()
    if rows:
        # Create a three-column grid layout
        for i in range(0, len(rows), 3):
            cols = st.columns(3)
            for j, col in enumerate(cols):
                if i + j < len(rows):
                    row = rows[i + j]
                    note_id, query, response, articles, videos, timestamp = row
                    article_links = [article for article in json.loads(articles)]
                    video_links = [video for video in json.loads(videos)]
                    title = response[:50]

                    with col:
                        if st.button(title, key=note_id):
                            st.session_state.selected_note_id = note_id
                            st.session_state.selected_note_content = {
                                "query": query,
                                "response": response,
                                "articles": article_links,
                                "videos": video_links
                            }
                            st.session_state.selected_note_timestamp = timestamp
                            st.rerun()
    else:
        st.markdown("No history available.")

def display_note_details():
    if "selected_note_id" in st.session_state:
        note_content = st.session_state.selected_note_content
        st.markdown(f"#### {note_content['query'].capitalize()}")
        with st.expander("artice"):
            articles_show(note_content['query'])
        with st.expander("video"):
            video_show(note_content['query'])
        st.markdown(f"** {st.session_state.selected_note_timestamp}**")
        st.markdown(f" {note_content['response']}")


# Database connection
conn = sqlite3.connect('history.db')
c = conn.cursor()

# Display the saved notes
display_saved_notes(c, conn)

# Display the details of the selected note
display_note_details()

# Close the database connection
conn.close()
