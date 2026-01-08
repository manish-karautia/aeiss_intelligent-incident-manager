def normalize_time_phrases(text: str) -> str:
    text = text.lower()
    replacements = {
        "24hrs": "24 hours",
        "24 hrs": "24 hours",
        "last day": "last 24 hours",
        "yesterday": "last 24 hours"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text
