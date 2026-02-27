import requests
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "schemes.db")


# ✅ Fetch webpage text
def fetch_webpage_text(url):
    try:
        response = requests.get(url)
        return response.text
    except Exception:
        return "Sample agricultural scheme announcement text."


# ✅ Simulated AI extraction
def extract_schemes_with_ai(raw_text):
    mock_response = [
        {
            "name": "AI Extracted PM-KISAN Scheme",
            "state": "Karnataka",
            "min_land": 0,
            "max_land": 10,
            "crop": "Rice",
            "category": "General",
            "income_limit": 500000,
            "subsidy": 7000,
            "documents": "Aadhar, Land Records",
            "deadline": "2026-12-31"
        }
    ]

    return json.dumps(mock_response)


# ✅ Save schemes safely (no duplicates)
def save_schemes_to_db(schemes_json):
    schemes = json.loads(schemes_json)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    for s in schemes:
        c.execute("SELECT * FROM schemes WHERE name = ?", (s["name"],))
        exists = c.fetchone()

        if exists:
            continue

        c.execute('''
        INSERT INTO schemes (
            name, state, min_land, max_land,
            crop, category, income_limit,
            subsidy, documents, deadline
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            s["name"],
            s["state"],
            s["min_land"],
            s["max_land"],
            s["crop"],
            s["category"],
            s["income_limit"],
            s["subsidy"],
            s["documents"],
            s["deadline"]
        ))

    conn.commit()
    conn.close()