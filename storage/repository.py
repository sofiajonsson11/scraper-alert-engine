from .db import get_connection


def save_item(title, price, url):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT OR IGNORE INTO users (title, price, url)
        VALUES (?, ?, ?)
    """,
        (title, price, url),
    )
    conn.commit()
    conn.close()


def items_exist(url):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE url = ?", (url,))
    result = cursor.fetchone()
    conn.close()
    return result is not None
