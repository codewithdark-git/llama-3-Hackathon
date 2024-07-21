import os
from together import Together


def generate_response(prompt):
    client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))
    try:
        response = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3-70B-Instruct-Lite",
            messages=[{'role': 'user', 'content': prompt}],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f'{e}'


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


def generate_file_response(query, chunk):
    prompt = f"""
    You are an AI assistant. A user has uploaded a file and asked the following question based on its content:
    User Query: "{query}"
    File Content: "{chunk}"
    Please provide a detailed and informative response based on the file content.
    """
    return prompt


def generate_from_file(chunk):
    prompt = f"""
    You are an AI assistant. A user has uploaded a file and wants to generate ideas or summaries based on its content.
    File Content: "{chunk}"
    Please provide a detailed summary and generate some innovative ideas based on the provided file content.
    """
    return prompt
