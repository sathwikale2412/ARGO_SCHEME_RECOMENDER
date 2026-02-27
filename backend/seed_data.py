import sqlite3
from models import init_db

def seed():
    init_db()

    conn = sqlite3.connect("schemes.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM schemes")

    schemes = [
        ("PM-KISAN", "Karnataka", 0, 10, "Rice", "General", 500000, 6000, "Aadhar, Land Records", "2026-03-31"),
        ("Rice Support Scheme", "Karnataka", 1, 12, "Rice", "OBC", 600000, 8000, "Aadhar, Caste Certificate", "2026-05-01"),
        ("Small Farmer Rice Grant", "Karnataka", 0, 8, "Rice", "General", 400000, 5000, "Land Records", "2026-06-15"),
        ("Crop Insurance Yojana", "Karnataka", 0, 20, "Wheat", "General", 800000, 10000, "Aadhar, Bank Passbook", "2026-02-15"),
        ("Drip Irrigation Subsidy", "Maharashtra", 1, 15, "Sugarcane", "OBC", 600000, 25000, "Land Records, Caste Certificate", "2026-04-01"),
    ]

    cursor.executemany("""
    INSERT INTO schemes (name, state, min_land, max_land, crop, category, income_limit, subsidy, documents, deadline)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, schemes)

    conn.commit()
    conn.close()

    print("Schemes inserted successfully!")

if __name__ == "__main__":
    seed()