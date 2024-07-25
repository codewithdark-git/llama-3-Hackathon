import sqlite3
import json

def init_db():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY,
            query TEXT,
            response TEXT,
            articles TEXT,
            videos TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def add_history(query, response, articles, videos):
    conn = sqlite3.connect('history.db')
    c = conn.cursor()

    # Convert lists or other structures to JSON strings
    articles_str = json.dumps(articles)
    videos_str = json.dumps(videos)

    c.execute('''
        INSERT INTO history (query, response, articles, videos)
        VALUES (?, ?, ?, ?)
    ''', (query, response, articles_str, videos_str))

    conn.commit()
    conn.close()


def get_history():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('SELECT query, response, articles, videos, timestamp FROM history ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()
    return rows
