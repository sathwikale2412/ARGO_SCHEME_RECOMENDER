import sqlite3
import random
from models import init_db

def seed():
    init_db()

    conn = sqlite3.connect("schemes.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM schemes")

    states_crops = {

        # 28 STATES
        "Andhra Pradesh": ["Rice", "Chilli", "Cotton"],
        "Arunachal Pradesh": ["Rice", "Maize", "Millets"],
        "Assam": ["Tea", "Rice", "Mustard"],
        "Bihar": ["Rice", "Wheat", "Maize"],
        "Chhattisgarh": ["Rice", "Maize", "Pulses"],
        "Goa": ["Rice", "Coconut", "Cashew"],
        "Gujarat": ["Cotton", "Groundnut", "Bajra"],
        "Haryana": ["Wheat", "Rice", "Cotton"],
        "Himachal Pradesh": ["Apple", "Maize", "Wheat"],
        "Jharkhand": ["Rice", "Maize", "Pulses"],
        "Karnataka": ["Rice", "Ragi", "Sugarcane"],
        "Kerala": ["Coconut", "Rubber", "Spices"],
        "Madhya Pradesh": ["Soybean", "Wheat", "Pulses"],
        "Maharashtra": ["Sugarcane", "Cotton", "Soybean"],
        "Manipur": ["Rice", "Maize", "Pulses"],
        "Meghalaya": ["Rice", "Potato", "Maize"],
        "Mizoram": ["Rice", "Oilseeds", "Maize"],
        "Nagaland": ["Rice", "Maize", "Millets"],
        "Odisha": ["Rice", "Pulses", "Oilseeds"],
        "Punjab": ["Wheat", "Rice", "Maize"],
        "Rajasthan": ["Bajra", "Wheat", "Mustard"],
        "Sikkim": ["Cardamom", "Maize", "Rice"],
        "Tamil Nadu": ["Rice", "Coconut", "Sugarcane"],
        "Telangana": ["Rice", "Cotton", "Maize"],
        "Tripura": ["Rice", "Rubber", "Tea"],
        "Uttar Pradesh": ["Wheat", "Rice", "Sugarcane"],
        "Uttarakhand": ["Rice", "Wheat", "Millets"],
        "West Bengal": ["Rice", "Jute", "Tea"],

        # 8 UNION TERRITORIES
        "Andaman and Nicobar Islands": ["Coconut", "Rice", "Spices"],
        "Chandigarh": ["Vegetables", "Wheat", "Rice"],
        "Dadra and Nagar Haveli and Daman and Diu": ["Rice", "Millets", "Pulses"],
        "Delhi": ["Vegetables", "Wheat", "Mustard"],
        "Jammu and Kashmir": ["Apple", "Rice", "Maize"],
        "Ladakh": ["Barley", "Wheat", "Millets"],
        "Lakshadweep": ["Coconut", "Rice", "Spices"],
        "Puducherry": ["Rice", "Sugarcane", "Coconut"]
    }

    central_schemes = {
        "PM-KISAN Samman Nidhi":
            "Provides income support of ₹6000 per year to eligible farmer families.",
        "Pradhan Mantri Fasal Bima Yojana (PMFBY)":
            "Crop insurance scheme protecting farmers against crop loss.",
        "Soil Health Card Scheme":
            "Provides soil nutrient reports and fertilizer recommendations.",
        "Agriculture Infrastructure Fund":
            "Supports development of farm infrastructure and storage facilities.",
        "National Food Security Mission":
            "Improves production of rice, wheat and pulses."
    }

    for state, crops in states_crops.items():
        for crop in crops:

            central_name = random.choice(list(central_schemes.keys()))

            schemes = [

                (
                    central_name,
                    state, 0, 20, crop,
                    "General",
                    800000,
                    random.randint(5000, 15000),
                    "Aadhar, Land Records",
                    "2026-12-31",
                    central_schemes[central_name]
                ),

                (
                    f"{state} {crop} Promotion Scheme",
                    state, 0, 20, crop,
                    "General",
                    800000,
                    random.randint(10000, 25000),
                    "Aadhar, Land Records",
                    "2026-12-31",
                    f"State government initiative to promote {crop} cultivation in {state}."
                ),

                (
                    f"{state} Farmer Welfare Scheme for {crop}",
                    state, 0, 20, crop,
                    "General",
                    800000,
                    random.randint(15000, 30000),
                    "Aadhar, Land Records",
                    "2026-12-31",
                    f"Financial assistance and subsidy support for {crop} farmers in {state}."
                )
            ]

            for scheme in schemes:
                cursor.execute("""
                INSERT INTO schemes
                (name, state, min_land, max_land, crop, category,
                 income_limit, subsidy, documents, deadline, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, scheme)

    conn.commit()
    conn.close()
    print("All India schemes generated successfully!")

if __name__ == "__main__":
    seed()