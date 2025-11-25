import sqlite3
import logging
from pathlib import Path

DB_FILE = Path("weather_data.db")


def init_db():
    """Initialize database and create table if it doesn't exist."""
    DB_FILE.parent.mkdir(exist_ok=True)  # Ensure parent folder exists
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


def save_weather(temperature: str, description: str, feels_like: str, url: str) -> None:
    """Save a weather record to the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "INSERT OR REPLACE INTO weather (temperature, description, feels_like, url) VALUES (?, ?, ?, ?)",
        (temperature, description, feels_like, url),
    )
    conn.commit()
    conn.close()
    logging.info(f"Saved weather record: {temperature}, {description}, {feels_like}")


def get_latest_weather(limit: int = 5):
    """Return the latest `limit` weather records."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM weather ORDER BY scraped_at DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows


def get_last_weather(url: str):
    """Return the most recent weather record for a specific URL."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "SELECT * FROM weather WHERE url=? ORDER BY scraped_at DESC LIMIT 1", (url,)
    )
    row = c.fetchone()
    conn.close()
    return row


def has_meaningful_change(new_data: dict, old_data: dict) -> bool:
    """Check if there is a meaningful change between old and new weather data."""
    if not old_data:
        return True
    return (
        new_data["temperature"] != old_data[1]  # old_data[1] = temperature
        or new_data["description"] != old_data[2]
        or new_data["feels_like"] != old_data[3]
    )
