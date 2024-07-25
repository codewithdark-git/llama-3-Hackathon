from utils.llm import generate_response, generate_file_response, generate_from_file
from utils.helper import split_text_into_chunks, read_file
from utils.common import articles_show, video_show
from app import local_css
import streamlit as st

local_css("pages/style.css")
st.page_link('app.py', label='Back To Home', icon="🏠")

# File upload
uploaded_file = st.file_uploader("Upload a file (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

if uploaded_file:
    file_content = read_file(uploaded_file)
    st.write("File content:")
    st.code(file_content[:100])  # Displaying first 1000 characters for preview

    # User choice for chat or generate ideas
    choice = st.radio("Choose an option", ("Chat with this file", "Generate ideas/text about this file"))


    if choice == "Chat with this file":
            query = st.chat_input("Ask me anything about the file")
            if query:
                with st.spinner("Generating response..."):
                    combined_response = ""
                    for chunk in split_text_into_chunks(file_content):
                        prompt = generate_file_response(query, chunk)
                        response_text = generate_response(prompt)
                        combined_response += response_text + "\n"
                    st.markdown(f'##### Response from the file')
                    query = query + file_content[:100]

                    with st.expander('Sources'):
                        articles_show(query)
                    with st.expander('Video Sources'):
                        video_show(query)

                    st.write(combined_response)
    elif choice == "Generate ideas/text about this file":
            with st.spinner("Generating ideas..."):
                combined_response = ""
                for chunk in split_text_into_chunks(file_content):
                    prompt = generate_from_file(chunk)
                    response_text = generate_response(prompt)
                    combined_response += response_text + "\n"
                st.markdown(f'##### Response ideas about the file')
                query = file_content[:100]
                with st.expander('Sources'):
                    articles_show(query)
                with st.expander('Video Sources'):
                    video_show(query)
                st.write(combined_response)


