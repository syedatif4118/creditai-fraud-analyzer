import sqlite3
from pathlib import Path

DB_PATH = Path("data/creditai.db")
DB_PATH.parent.mkdir(exist_ok=True)


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_type TEXT,
            extracted_text TEXT,
            source_file TEXT
        )
    """)

    conn.commit()
    conn.close()
