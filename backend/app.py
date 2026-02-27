from flask import Flask, request, jsonify
from flask_cors import CORS
from recommender import recommend
import sqlite3

app = Flask(__name__)
CORS(app)


# ---------------- GET SCHEMES ----------------
@app.route("/get_schemes", methods=["POST"])
def get_schemes():
    data = request.get_json()
    results = recommend(data)
    return jsonify(results)


# ---------------- CHAT ROUTE ----------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip().lower()

    conn = sqlite3.connect("schemes.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM schemes")
    schemes = cursor.fetchall()

    results = []

    for scheme in schemes:
        scheme_state = scheme["state"].lower()
        scheme_crop = scheme["crop"].lower()

        if message in scheme_state or message in scheme_crop:
            results.append({
                "name": scheme["name"],
                "subsidy": scheme["subsidy"],
                "deadline": scheme["deadline"],
                "description": scheme["description"]
            })

    conn.close()

    if results:
        return jsonify({
            "reply": f"Found {len(results)} schemes for '{message}':",
            "schemes": results
        })
    else:
        return jsonify({
            "reply": f"No schemes found for '{message}'.",
            "schemes": []
        })


if __name__ == "__main__":
    app.run(debug=True, port=5000)