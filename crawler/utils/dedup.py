import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'dedup.db')


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS published (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id TEXT UNIQUE NOT NULL,
            title TEXT,
            published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn


def is_published(item_id: str) -> bool:
    conn = _get_conn()
    cur = conn.execute('SELECT 1 FROM published WHERE item_id = ?', (item_id,))
    result = cur.fetchone() is not None
    conn.close()
    return result


def mark_published(item_id: str, title: str = ''):
    conn = _get_conn()
    try:
        conn.execute('INSERT INTO published (item_id, title) VALUES (?, ?)', (item_id, title))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()
