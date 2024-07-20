import urllib.parse
from googlesearch import search
from youtubesearchpython import VideosSearch
import PyPDF2
import docx


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


def fetch_videos(query):
    videos_search = VideosSearch(query, limit=6)
    return videos_search.result()['result']


def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def read_file(file):
    if file.type == "application/pdf":
        return read_pdf(file)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return read_docx(file)
    elif file.type == "text/plain":
        return file.read().decode("utf-8")
    else:
        return "Unsupported file type"


def read_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])


def split_text_into_chunks(text, chunk_size=3000):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i + chunk_size])
