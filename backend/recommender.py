import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "schemes.db")

def recommend(data):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM schemes")
    schemes = cursor.fetchall()

    results = []

    user_state = str(data.get("state") or data.get("State") or "").strip().lower()
    user_crop = str(data.get("crop") or data.get("Crop") or "").strip().lower()
    user_category = str(data.get("category") or data.get("Category") or "").strip().lower()
    user_land = float(data.get("land") or data.get("Land") or 0)
    user_income = float(data.get("income") or data.get("Income") or 0)

    for scheme in schemes:
        scheme_state = scheme["state"].strip().lower()
        scheme_crop = scheme["crop"].strip().lower()
        scheme_category = scheme["category"].strip().lower()
        min_land = scheme["min_land"]
        max_land = scheme["max_land"]
        income_limit = scheme["income_limit"]

        if (
            user_state in scheme_state and
            user_crop in scheme_crop and
            user_category == scheme_category and
            min_land <= user_land <= max_land and
            user_income <= income_limit
        ):
            results.append({
                "name": scheme["name"],
                "subsidy": scheme["subsidy"],
                "documents": scheme["documents"],
                "deadline": scheme["deadline"]
            })

    conn.close()
    return results