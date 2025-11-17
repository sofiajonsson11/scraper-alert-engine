import sqlite3
from storage.db import DB_FILE


def save_item(temperature, description, feels_like, url):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        """
        INSERT OR IGNORE INTO weather (temperature, description, feels_like, url)
        VALUES (?, ?, ?, ?)
    """,
        (temperature, description, feels_like, url),
    )
    conn.commit()
    conn.close()


def item_exists(url, description, temperature):
    """Checik if the same weather record already exists in the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM weather WHERE url=? AND description=? AND temperature=?",
        (url, description, temperature),
    )
    result = cursor.fetchone()
    conn.close()
    return bool(result)


def get_latest_items(limit=5):
    """Fetch the latest rows from the weather table."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "SELECT id, temperature, description, feels_like, url, scraped_at FROM weather ORDER BY scraped_at DESC LIMIT ?",
        (limit,),
    )
    rows = c.fetchall()
    conn.close()
    return rows
