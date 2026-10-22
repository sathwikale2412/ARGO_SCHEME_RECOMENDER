"""Scheme matching rules.

State, crop, land and income use the original backend/recommender.py predicate verbatim.
Only the category comparison was changed (2026-10-22, at the owner's request): it used to
be an exact string test, so "SC" or "Small and Marginal" matched nothing even though the
catalogue has those rows. `_category_key()` plus `_category_matches()` below resolve the
common spellings and near-misses instead, and stay closed to anything that is not clearly
one of them — a wrong category silently matching would hand a farmer the wrong advice.
"""

import difflib
import re

# Folded category spellings that mean the same row group. Keys are the normalised form
# produced by _category_key(); keep this list to genuine synonyms and abbreviations.
_CATEGORY_ALIASES = {
    "sc": "scst", "st": "scst", "caste": "scst", "tribe": "scst", "tribal": "scst",
    "schedulecaste": "scst", "scheduledtribe": "scst", "scsttribal": "scst",
    "obc": "obc", "backwardsclass": "obc",
    "gen": "general", "general": "general", "open": "general", "unreserved": "general",
    "women": "women", "woman": "women", "female": "women",
    "youth": "youth", "young": "youth", "younger": "youth",
    "small": "smallmarginal", "marginal": "smallmarginal", "smallholder": "smallmarginal",
    "tenant": "tenantfarmer", "tenancy": "tenantfarmer", "lease": "tenantfarmer",
    "organic": "organic", "natural": "organic", "naturalfarming": "organic",
}

_PUNCTUATION = re.compile(r"[^a-z0-9]+")


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


def _category_key(text):
    """Fold a category name into the form the alias table speaks: no spaces, no
    punctuation, no filler 'and'."""
    folded = _PUNCTUATION.sub("", str(text or "").lower().replace(" and ", " "))
    return _CATEGORY_ALIASES.get(folded, folded)


def _category_matches(user_value, scheme_value):
    """True when a typed category clearly names the scheme's category.

    Exact after folding, one value being the other's prefix (so "women farmer" is Women),
    or a close spelling ("tenent farmer"). The fuzzy step needs a high ratio on purpose:
    matching across two different eligibility groups would return advice for a scheme the
    farmer is not in, which is worse than the empty result the page explains.
    """
    if not user_value:
        return False
    scheme_key = _category_key(scheme_value)
    if user_value == scheme_key:
        return True
    shortest, longest = sorted((user_value, scheme_key), key=len)
    if len(shortest) >= 4 and longest.startswith(shortest):
        return True
    return difflib.SequenceMatcher(None, user_value, scheme_key).ratio() >= 0.8


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
    user_category = _category_key(text_field(data, "category", "Category"))
    user_land = _to_float(data.get("land") or data.get("Land"))
    user_income = _to_float(data.get("income") or data.get("Income"))

    if user_land is None or user_income is None:
        return []

    results = []

    for scheme in schemes:
        scheme_state = str(scheme.get("state") or "").strip().lower()
        scheme_crop = str(scheme.get("crop") or "").strip().lower()
        min_land = _to_float(scheme.get("min_land")) or 0.0
        max_land = _to_float(scheme.get("max_land")) or 0.0
        income_limit = _to_float(scheme.get("income_limit")) or 0.0

        if (
            user_state in scheme_state
            and user_crop in scheme_crop
            and _category_matches(user_category, scheme.get("category"))
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
