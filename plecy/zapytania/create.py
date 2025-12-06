
from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "db" / "baza.db"

DB_PATH.parent.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );
    """
)

cur.execute("DELETE FROM users;")
cur.execute(
    "INSERT INTO users (login, password) VALUES (?, ?);",
    ("admin", "haslo"),
)

conn.commit()
conn.close()

print("Baza utworzona w:", DB_PATH)

