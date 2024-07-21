### Docker Container
- pull from docker and used free llama 3 
```commandline
    docker pull codewithdark/llama3-hackathon:new
```
# LLaMA Genius || AI Research Assistant

LLaMA Genius is an AI-powered research assistant designed to help users interact with and extract insights from various sources, including uploaded files and web content. This application leverages advanced AI models to provide meaningful responses, generate ideas, and fetch relevant articles and videos.

## Features Overview

### 1. Chat with File
- **File Upload**: Allows users to upload PDF, DOCX, and TXT files.
- **File Reading**: Reads and extracts text from the uploaded files.
- **Text Chunking**: Splits the text into manageable chunks for processing.
- **AI Interaction**: Users can either chat with the file content or generate ideas/text about the file using an AI model.
- **Navigation**: Links to navigate back to the home page and to the "Chat with Web" feature.

### 2. Chat with Web
- **Query Input**: Users can input a query to get responses.
- **AI Response**: Generates a response to the user's query using an AI model.
- **Article Fetching**: Fetches articles related to the query using Google search.
- **YouTube Videos**: Fetches YouTube videos related to the query.
- **Sources Display**: Displays the fetched articles and videos.
- **Navigation**: Links to navigate back to the home page and to the "Chat with File" feature.

## How to Use

### Chat with File
1. Go to the "Chat with File" page.
2. Upload a file (PDF, DOCX, or TXT).
3. Choose to either chat with the file content or generate ideas/text about the file.
4. If chatting, input your query and get responses based on the file content.
5. If generating ideas, get summarized ideas or text about the file content.

### Chat with Web
1. Go to the "Chat with Web" page.
2. Input your query in the chat box.
3. Get AI-generated responses along with related articles and YouTube videos.
4. Explore sources by expanding the 'Sources' and 'Video Sources' sections.

## Installation

To run this application locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/codewithdark-git/llama-genius.git
    cd llama-genius
    ```

2. **Create a virtual environment and activate it**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Streamlit app**:
    ```bash
    streamlit run app.py
    ```

## Project Structure

- `app.py`: The main entry point of the application. It contains the home page with navigation links and documentation.
- `pages/chatWithFile.py`: Handles the "Chat with File" functionality, including file upload, text extraction, and AI interaction.
- `pages/chatWithWeb.py`: Handles the "Chat with Web" functionality, including query input, AI response, and fetching related articles and YouTube videos.
- `pages/style.css`: Custom CSS for styling the application.


## Collaborate

We welcome contributions from the community! If you're interested in contributing to LLaMA Genius, please follow these steps:

1. **Fork the repository**: Click the "Fork" button at the top right corner of this repository to create a copy of it in your GitHub account.

2. **Clone your forked repository**:
3. **Create a new branch**: Create a new branch for your feature or bugfix.
    ```bash
    git checkout -b feature-name
    ```

4. **Make your changes**: Implement your feature or fix the bug. Ensure your code follows the project's coding standards.

5. **Commit your changes**: Write a clear and concise commit message.
    ```bash
    git add .
    git commit -m "Description of the feature or fix"
    ```

6. **Push to your branch**:
    ```bash
    git push origin feature-name
    ```

7. **Create a Pull Request**: Go to the original repository and click on the "New Pull Request" button. Provide a detailed description of your changes and submit the pull request.

### Guidelines for Contributions

- **Code Quality**: Ensure your code is well-documented and follows the project's coding standards.
- **Testing**: Test your changes thoroughly before submitting a pull request.
- **Issue Reporting**: If you find a bug or have a feature request, please create an issue in the issue tracker.
- **Discussions**: Feel free to start a discussion in the issues or pull requests if you have any questions or need clarification.

### license
MIT