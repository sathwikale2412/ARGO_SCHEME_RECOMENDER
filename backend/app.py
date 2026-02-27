from flask import Flask, request, jsonify
from flask_cors import CORS
from recommender import recommend

app = Flask(__name__)
CORS(app)   # ✅ Enable CORS

@app.route("/get_schemes", methods=["POST"])
def get_schemes():
    data = request.get_json()
    results = recommend(data)
    return jsonify(results)
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").lower()

    import sqlite3
    conn = sqlite3.connect("schemes.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM schemes")
    schemes = cursor.fetchall()

    results = []

    for scheme in schemes:
        if (
            message in scheme["state"].lower()
            or message in scheme["crop"].lower()
            or message in scheme["category"].lower()
        ):
            results.append({
                "name": scheme["name"],
                "subsidy": scheme["subsidy"],
                "deadline": scheme["deadline"]
            })

    conn.close()

    if results:
        return jsonify({
            "reply": "Here are matching schemes:",
            "schemes": results
        })
    else:
        return jsonify({
            "reply": "No schemes found for your query.",
            "schemes": []
        })

if __name__ == "__main__":
    app.run(debug=True, port=5000)