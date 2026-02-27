import sqlite3

DB_NAME = "schemes.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schemes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        state TEXT,
        min_land REAL,
        max_land REAL,
        crop TEXT,
        category TEXT,
        income_limit REAL,
        subsidy REAL,
        documents TEXT,
        deadline TEXT
    )
    """)

    conn.commit()
    conn.close()