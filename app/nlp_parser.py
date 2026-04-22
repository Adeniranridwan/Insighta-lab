import re

# Country name → ISO code map (extend as needed for your dataset)
COUNTRY_MAP = {
    "nigeria": "NG", "ghana": "GH", "kenya": "KE", "angola": "AO",
    "tanzania": "TZ", "ethiopia": "ET", "cameroon": "CM", "uganda": "UG",
    "senegal": "SN", "mali": "ML", "niger": "NE", "benin": "BJ",
    "togo": "TG", "ivory coast": "CI", "côte d'ivoire": "CI",
    "south africa": "ZA", "egypt": "EG", "morocco": "MA", "algeria": "DZ",
    "mozambique": "MZ", "zambia": "ZM", "zimbabwe": "ZW",
    "rwanda": "RW", "somalia": "SO", "sudan": "SD", "chad": "TD",
}

AGE_GROUP_MAP = {
    "child": "child",
    "children": "child",
    "teenager": "teenager",
    "teenagers": "teenager",
    "teen": "teenager",
    "teens": "teenager",
    "adult": "adult",
    "adults": "adult",
    "senior": "senior",
    "seniors": "senior",
    "elderly": "senior",
}

def parse_nl_query(q: str) -> dict | None:
    """
    Parse a plain English query into filter dict.
    Returns None if the query cannot be interpreted at all.
    """
    q = q.lower().strip()
    filters = {}
    matched_something = False

    # --- Gender ---
    if re.search(r'\bmales?\b', q):
        filters["gender"] = "male"
        matched_something = True
    elif re.search(r'\bfemales?\b|\bwomen\b|\bwoman\b|\bgirls?\b', q):
        filters["gender"] = "female"
        matched_something = True

    # --- "young" → ages 16–24 (parsing only, not a stored age_group) ---
    if re.search(r'\byoung\b', q):
        filters["min_age"] = 16
        filters["max_age"] = 24
        matched_something = True

    # --- Age group keywords ---
    for keyword, group in AGE_GROUP_MAP.items():
        if re.search(rf'\b{keyword}\b', q):
            filters["age_group"] = group
            matched_something = True
            break

    # --- "above X" / "over X" / "older than X" → min_age ---
    m = re.search(r'\b(?:above|over|older than)\s+(\d+)', q)
    if m:
        filters["min_age"] = int(m.group(1))
        matched_something = True

    # --- "below X" / "under X" / "younger than X" → max_age ---
    m = re.search(r'\b(?:below|under|younger than)\s+(\d+)', q)
    if m:
        filters["max_age"] = int(m.group(1))
        matched_something = True

    # --- "aged X" or "age X" → exact age (set both min and max) ---
    m = re.search(r'\b(?:aged?)\s+(\d+)', q)
    if m:
        age = int(m.group(1))
        filters["min_age"] = age
        filters["max_age"] = age
        matched_something = True

    # --- Country: "from <country>" or "in <country>" ---
    m = re.search(r'\b(?:from|in)\s+([a-z\s\']+?)(?:\s*$|\s+(?:and|who|with|aged|above|below|over|under))', q)
    if m:
        country_raw = m.group(1).strip()
        country_id = COUNTRY_MAP.get(country_raw)
        if country_id:
            filters["country_id"] = country_id
            matched_something = True

    if not matched_something:
        return None

    return filters