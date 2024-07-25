import streamlit as st

# Set page configuration
st.set_page_config(page_title="LLaMA Genius || AI Research Assistant", page_icon="random", initial_sidebar_state="collapsed")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load custom CSS
local_css("pages/style.css")


# Main function
def main():
    st.markdown('<div class="main-title">LLaMA Genius</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">By <a href="https://github.com/codewithdark-git" target="_blank">Dark Coder</a></div>', unsafe_allow_html=True)

    st.write('Choose Your Choice 🪧:')
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('Chat With File'):
            st.switch_page("pages/chatWithFile.py")
    with col2:
        if st.button('Chat With Web'):
            st.switch_page("pages/chatWithWeb.py")
    with col3:
        if st.button('See History'):
            st.switch_page("pages/history.py")

    st.markdown("""
        <div class="section-title">Features Overview</div>
        <p>This AI Research Assistant application provides two main functionalities:</p>

        <div class="section-title">1. Chat with File</div>
        <ul>
            <li><b>File Upload:</b> Allows users to upload PDF, DOCX, and TXT files.</li>
            <li><b>File Reading:</b> Reads and extracts text from the uploaded files.</li>
            <li><b>Text Chunking:</b> Splits the text into manageable chunks for processing.</li>
            <li><b>AI Interaction:</b> Users can either chat with the file content or generate ideas/text about the file using an AI model.</li>
            <li><b>Navigation:</b> Links to navigate back to the home page and to the "Chat with Web" feature.</li>
        </ul>

        <div class="section-title">2. Chat with Web</div>
        <ul>
            <li><b>Query Input:</b> Users can input a query to get responses.</li>
            <li><b>AI Response:</b> Generates a response to the user's query using an AI model.</li>
            <li><b>Article Fetching:</b> Fetches articles related to the query using Google search.</li>
            <li><b>YouTube Videos:</b> Fetches YouTube videos related to the query.</li>
            <li><b>Sources Display:</b> Displays the fetched articles and videos.</li>
            <li><b>Navigation:</b> Links to navigate back to the home page and to the "Chat with File" feature.</li>
        </ul>

        <div class="section-title">How to Use</div>
        <ol>
            <li><b>Chat with File:</b>
                <ol>
                    <li>Go to the "Chat with File" page.</li>
                    <li>Upload a file (PDF, DOCX, or TXT).</li>
                    <li>Choose to either chat with the file content or generate ideas/text about the file.</li>
                    <li>If chatting, input your query and get responses based on the file content.</li>
                    <li>If generating ideas, get summarized ideas or text about the file content.</li>
                </ol>
            </li>
            <li><b>Chat with Web:</b>
                <ol>
                    <li>Go to the "Chat with Web" page.</li>
                    <li>Input your query in the chat box.</li>
                    <li>Get AI-generated responses along with related articles and YouTube videos.</li>
                    <li>Explore sources by expanding the 'Sources' and 'Video Sources' sections.</li>
                </ol>
            </li>
        </ol>

        <div class="about-developer">
            <h3>About Developer</h3>
            <p><b>Name:</b> Dark Coder</p>
            <p><b>Email:</b> codewithdark90@gmail.com</p>
            <p><b>GitHub:</b> <a href="https://github.com/codewithdark-git" target="_blank">github.com/codewithdark-git</a></p>
            <p><b>LinkedIn:</b> <a href="https://www.linkedin.com/in/codewithdark/" target="_blank">linkedin.com/in/codewithdark</a></p>
            <p><b>Description:</b>
            Experienced developer with a passion for AI and machine learning. Skilled in developing AI-driven applications and integrating various APIs.</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
