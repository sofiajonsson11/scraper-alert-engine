import sqlite3
import logging
import os

DB_FILE = "weather_data.db"


def init_db():
    """Initialize the SQLite database and weather table."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature TEXT,
            description TEXT,
            feels_like TEXT,
            url TEXT UNIQUE,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()
    logging.info("Database initialized.")


def save_weather(data: dict):
    """
    Save a new weather record to the database.

    Args:
        data: Dict with keys 'temperature', 'description', 'feels_like', 'url'
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute(
            """
            INSERT INTO weather (temperature, description, feels_like, url)
            VALUES (?, ?, ?, ?)
            """,
            (data["temperature"], data["description"], data["feels_like"], data["url"]),
        )
        conn.commit()
        logging.info(
            f"Saved weather record: {data['temperature']}, {data['description']}, {data['feels_like']}"
        )
    except sqlite3.IntegrityError:
        logging.warning(f"Weather for URL already exists: {data['url']}")
    finally:
        conn.close()


def get_last_weather():
    """
    Fetch the most recent weather record from the database.

    Returns:
        dict or None: Most recent weather record, or None if table is empty.
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "SELECT temperature, description, feels_like, url FROM weather ORDER BY scraped_at DESC LIMIT 1"
    )
    row = c.fetchone()
    conn.close()

    if row:
        return {
            "temperature": row[0],
            "description": row[1],
            "feels_like": row[2],
            "url": row[3],
        }
    return None


def has_meaningful_change(new_data: dict, old_data: dict | None) -> bool:
    """
    Determine if new weather data differs from the last record.

    Args:
        new_data: Latest weather scrape
        old_data: Last weather record from DB

    Returns:
        bool: True if there is a meaningful change
    """
    if not old_data:
        return True
    return (
        new_data["temperature"] != old_data["temperature"]
        or new_data["description"] != old_data["description"]
        or new_data["feels_like"] != old_data["feels_like"]
    )
