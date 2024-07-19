import streamlit as st
import PyPDF2
import docx
import asyncio
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

# Function to read text from uploaded files
def read_file(file):
    if file.type == "application/pdf":
        return read_pdf(file)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return read_docx(file)
    elif file.type == "text/plain":
        return file.read().decode("utf-8")
    else:
        return "Unsupported file type"

# Function to read PDF files
def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Function to read DOCX files
def read_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# Function to split text into chunks
def split_text_into_chunks(text, chunk_size=3000):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i + chunk_size])

# Streamlit app
st.set_page_config(page_title="AI Research Assistant with File Upload")
st.page_link('app.py', label='Home', icon="🏠")


# File upload
uploaded_file = st.file_uploader("Upload a file (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

if uploaded_file:
    file_content = read_file(uploaded_file)
    st.write("File content:")
    st.code(file_content[:100])  # Displaying first 1000 characters for preview

    # User choice for chat or generate ideas
    choice = st.radio("Choose an option", ("Chat with this file", "Generate ideas/text about this file"))

    if st.button("Proceed"):
        if choice == "Chat with this file":
            query = st.text_input("Ask me anything about the file")
            if query:
                with st.spinner("Generating response..."):
                    combined_response = ""
                    for chunk in split_text_into_chunks(file_content):
                        response_text = asyncio.run(generate_response(f"{query}\n\n{chunk}"))
                        combined_response += response_text + "\n"
                    st.write(combined_response)
        elif choice == "Generate ideas/text about this file":
            with st.spinner("Generating ideas..."):
                combined_response = ""
                for chunk in split_text_into_chunks(file_content):
                    response_text = asyncio.run(generate_response(f"Generate ideas or summary for the following text:\n\n{chunk}"))
                    combined_response += response_text + "\n"
                st.write(combined_response)
