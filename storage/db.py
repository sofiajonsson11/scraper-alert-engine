import sqlite3
import logging

DB_PATH = "weather.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS weather_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            provider TEXT,
            temperature TEXT,
            description TEXT,
            feels_like TEXT,
            url TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    conn.commit()
    conn.close()
    logging.info("Database initialized.")


def save_weather(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO weather_history (provider, temperature, description, feels_like, url)
        VALUES (?, ?, ?, ?, ?)
    """,
        (
            data.get("provider"),
            data.get("temperature"),
            data.get("description"),
            data.get("feels_like"),
            data.get("url"),
        ),
    )
    conn.commit()
    conn.close()
