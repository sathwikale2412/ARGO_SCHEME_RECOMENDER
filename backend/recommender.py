import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "schemes.db")

def recommend(data):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM schemes")
    schemes = cursor.fetchall()

    user_state = str(data.get("state", "")).strip().lower()
    user_crop = str(data.get("crop", "")).strip().lower()

    results = []

    for scheme in schemes:
        scheme_state = scheme["state"].strip().lower()
        scheme_crop = scheme["crop"].strip().lower()

        # EXACT MATCH
        if user_state == scheme_state and user_crop == scheme_crop:
            results.append({
                "name": scheme["name"],
                "subsidy": scheme["subsidy"],
                "documents": scheme["documents"],
                "deadline": scheme["deadline"],
                "description": scheme["description"]
            })

    conn.close()
    return results