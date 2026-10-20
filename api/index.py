"""ARGO API — the Flask app from backend/app.py, packaged for serverless.

One catch-all route dispatches on the trailing path segment, so the same module answers
`/get_schemes` when run with `flask run` locally and `/api/get_schemes` on Vercel,
without hardcoding a mount prefix.

Removed from the original: `debug=True` (the Werkzeug debugger is a remote-code-execution
surface) and the SQLite connection (an ephemeral filesystem cannot hold the catalogue).
"""

import time
import uuid

from flask import Flask, jsonify, request

import recommender
from supabase_client import NotConfigured, fetch_schemes, is_configured

app = Flask(__name__)

# Anyone who opens the site can reach these endpoints, and each one reads the whole
# catalogue. The counter lives in one warm instance, so it slows a scripted visitor down
# rather than guaranteeing a limit — a stateless function cannot share one counter.
RATE_WINDOW_SECONDS = 60
RATE_MAX_REQUESTS = 30

_hits: dict[str, list[float]] = {}


def _caller_key():
    forwarded = request.headers.get("X-Forwarded-For", "")
    return forwarded.split(",")[0].strip() or request.remote_addr or "unknown"


def rate_limited(key):
    now = time.time()
    hits = [seen for seen in _hits.get(key, []) if now - seen < RATE_WINDOW_SECONDS]
    if len(hits) >= RATE_MAX_REQUESTS:
        _hits[key] = hits
        return True
    hits.append(now)
    _hits[key] = hits
    return False


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

    if rate_limited(_caller_key()):
        return jsonify(
            {
                "status": "error",
                "message": f"Too many requests from this address. Wait {RATE_WINDOW_SECONDS} seconds.",
                "ref": uuid.uuid4().hex[:8],
            }
        ), 429

    if action == "get_schemes":
        problem = recommender.validate_search(_body())
        if problem:
            return jsonify({"status": "error", "message": problem}), 400

    if action == "chat":
        message = _body().get("message", "")
        if not isinstance(message, str) or not message.strip() or len(message) > 500:
            return jsonify(
                {"status": "error", "message": "message must be text, 1-500 characters."}
            ), 400

    try:
        schemes = fetch_schemes()

        if action == "schemes":
            return jsonify({"count": len(schemes), "schemes": schemes})

        if action == "get_schemes":
            return jsonify({"status": "ok", "results": recommender.recommend(_body(), schemes)})

        results = recommender.search_by_keyword(_body().get("message", ""), schemes)
        if results:
            return jsonify({"reply": "Here are matching schemes:", "schemes": results})
        return jsonify({"reply": "No schemes found for your query.", "schemes": []})

    except NotConfigured as err:
        return jsonify({"status": "unavailable", "message": str(err)}), 503
    except Exception:  # noqa: BLE001
        # The traceback goes to the platform log, never to the caller: an exception message
        # repeats the SQL fragment or PostgREST body that set it off, and this endpoint is
        # unauthenticated, so a visitor would be reading the catalogue's internals.
        reference = uuid.uuid4().hex[:8]
        app.logger.exception("ARGO API request failed (ref %s)", reference)
        return jsonify(
            {
                "status": "error",
                "message": "The scheme catalogue could not be searched. Try again shortly.",
                "ref": reference,
            }
        ), 500
