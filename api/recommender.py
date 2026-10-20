"""Scheme matching rules.

The predicate is the one the original backend/recommender.py used, kept verbatim so
eligibility behaviour does not drift: state and crop are substring matches, category is
an exact match, and land/income are range checks. Only the data source changed — rows
come from Postgres through PostgREST instead of a local SQLite file.
"""


def _to_float(value):
    """Parse loosely — '5 acres' is 5.0. Returns None when there is no number at all."""
    if value is None or str(value).strip() == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        digits = "".join(c for c in str(value) if c.isdigit() or c == ".")
        try:
            return float(digits) if digits else None
        except ValueError:
            return None


def text_field(data, *names):
    for name in names:
        value = data.get(name)
        if value:
            return str(value).strip().lower()
    return ""


def validate_search(data):
    """Return a readable problem, or None when the search inputs are usable.

    Garbage must not be silently read as 0 acres — a typo would come back as a
    confident, wrong eligibility answer.
    """
    for field in ("state", "crop", "category"):
        if not str(data.get(field) or "").strip():
            return f"'{field}' is required."
    for field in ("land", "income"):
        raw = data.get(field)
        if raw is None or str(raw).strip() == "":
            return f"'{field}' is required."
        value = _to_float(raw)
        if value is None:
            return f"'{field}' must be a number."
        if value < 0:
            return f"'{field}' cannot be negative."
    return None


def recommend(data, schemes):
    user_state = text_field(data, "state", "State")
    user_crop = text_field(data, "crop", "Crop")
    user_category = text_field(data, "category", "Category")
    user_land = _to_float(data.get("land") or data.get("Land"))
    user_income = _to_float(data.get("income") or data.get("Income"))

    if user_land is None or user_income is None:
        return []

    results = []

    for scheme in schemes:
        scheme_state = str(scheme.get("state") or "").strip().lower()
        scheme_crop = str(scheme.get("crop") or "").strip().lower()
        scheme_category = str(scheme.get("category") or "").strip().lower()
        min_land = _to_float(scheme.get("min_land")) or 0.0
        max_land = _to_float(scheme.get("max_land")) or 0.0
        income_limit = _to_float(scheme.get("income_limit")) or 0.0

        if (
            user_state in scheme_state
            and user_crop in scheme_crop
            and user_category == scheme_category
            and min_land <= user_land <= max_land
            and user_income <= income_limit
        ):
            results.append(
                {
                    "name": scheme.get("name"),
                    "subsidy": scheme.get("subsidy"),
                    "documents": scheme.get("documents"),
                    "deadline": scheme.get("deadline"),
                }
            )

    return results


def search_by_keyword(message, schemes):
    message = (message or "").strip().lower()
    results = []

    if not message:
        return results

    for scheme in schemes:
        haystack = [
            str(scheme.get("state") or "").lower(),
            str(scheme.get("crop") or "").lower(),
            str(scheme.get("category") or "").lower(),
        ]
        if any(message in field for field in haystack):
            results.append(
                {
                    "name": scheme.get("name"),
                    "subsidy": scheme.get("subsidy"),
                    "deadline": scheme.get("deadline"),
                }
            )

    return results
