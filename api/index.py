"""ARGO API — the Flask app from backend/app.py, packaged for serverless.

One catch-all route dispatches on the trailing path segment, so the same module answers
`/get_schemes` when run with `flask run` locally and `/api/get_schemes` on Vercel,
without hardcoding a mount prefix.

Removed from the original: `debug=True` (the Werkzeug debugger is a remote-code-execution
surface) and the SQLite connection (an ephemeral filesystem cannot hold the catalogue).
"""

from flask import Flask, jsonify, request

import recommender
from supabase_client import NotConfigured, fetch_schemes, is_configured

app = Flask(__name__)


def _body():
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}


@app.route("/", defaults={"path": ""}, methods=["GET", "POST"])
@app.route("/<path:path>", methods=["GET", "POST"])
def gateway(path):
    action = path.rstrip("/").split("/")[-1]

    if action in ("", "health"):
        return jsonify(
            {
                "status": "ok",
                "service": "argo-api",
                "database": "configured" if is_configured() else "missing env",
            }
        )

    if action == "schemes" and request.method == "POST":
        return jsonify(
            {
                "status": "error",
                "message": (
                    "Add schemes from the signed-in browser session, not this endpoint: "
                    "the function calls PostgREST with the anon key, so Row Level Security "
                    "cannot see a user and the insert would be rejected."
                ),
            }
        ), 405

    if action not in ("schemes", "get_schemes", "chat"):
        return jsonify({"status": "error", "message": f"Unknown endpoint: /{action}"}), 404

    if action == "get_schemes":
        problem = recommender.validate_search(_body())
        if problem:
            return jsonify({"status": "error", "message": problem}), 400

    try:
        schemes = fetch_schemes()

        if action == "schemes":
            return jsonify({"count": len(schemes), "schemes": schemes})

        if action == "get_schemes":
            return jsonify({"status": "ok", "results": recommender.recommend(_body(), schemes)})

        message = _body().get("message", "")
        results = recommender.search_by_keyword(message, schemes)
        if results:
            return jsonify({"reply": "Here are matching schemes:", "schemes": results})
        return jsonify({"reply": "No schemes found for your query.", "schemes": []})

    except NotConfigured as err:
        return jsonify({"status": "unavailable", "message": str(err)}), 503
    except Exception as err:  # noqa: BLE001 - never leak a traceback to the client
        app.logger.exception("ARGO API request failed")
        return jsonify({"status": "error", "message": f"{type(err).__name__}: {err}"}), 500
