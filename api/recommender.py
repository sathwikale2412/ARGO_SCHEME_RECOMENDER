"""Scheme matching rules.

State, crop, land and income use the original backend/recommender.py predicate verbatim.
Only the category comparison was changed (2026-10-22, at the owner's request): it used to
be an exact string test, so "SC" or "Small and Marginal" matched nothing even though the
catalogue has those rows. `_category_key()` plus `_category_matches()` below resolve the
common spellings and near-misses instead, and stay closed to anything that is not clearly
one of them — a wrong category silently matching would hand a farmer the wrong advice.
`search_by_keyword()` no longer mirrors its original either (2026-10-23): the inherited
version required the entire question to sit inside one field, so every multi-word question
came back empty. See its docstring.
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


# Words a farmer uses to ask, not to filter. Left in, they would match half the catalogue.
_SEARCH_STOPWORDS = frozenset({
    "i", "a", "am", "an", "are", "any", "about", "applicable", "available", "can", "could",
    "do", "does", "find", "for", "from", "get", "how", "is", "in", "list", "me", "my",
    "need", "of", "on", "please", "scheme", "schemes", "should", "show", "tell", "that",
    "the", "there", "this", "to", "want", "we", "what", "when", "where", "which", "who",
    "why", "will", "with", "would", "you", "your",
})


def search_by_keyword(message, schemes):
    """Rank the catalogue against a free-text question.

    The original predicate tested whether the whole message sat inside one field, so
    "drip irrigation in Maharashtra" matched nothing even though the catalogue holds that
    row; only a single word fully contained in state, crop or category ever returned.
    Words are matched instead, across the scheme name as well, and the rows holding more
    of them come first.
    """
    message = (message or "").strip().lower()
    words = [word for word in re.split(r"[^a-z0-9/&]+", message)
             if word and word not in _SEARCH_STOPWORDS]
    if not words:
        return []

    scored = []
    for position, scheme in enumerate(schemes):
        haystack = " ".join((
            str(scheme.get("name") or ""),
            str(scheme.get("state") or ""),
            str(scheme.get("crop") or ""),
            str(scheme.get("category") or ""),
        )).lower()
        hits = sum(1 for word in words if word in haystack)
        if hits:
            scored.append((hits, position, scheme))

    scored.sort(key=lambda row: (-row[0], row[1]))
    return [
        {
            "name": scheme.get("name"),
            "subsidy": scheme.get("subsidy"),
            "deadline": scheme.get("deadline"),
        }
        for _hits, _position, scheme in scored[:10]
    ]
