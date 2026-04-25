import re

def clean_query(text: str):
    if not text:
        return text

    # 1. Remove emojis (safe Unicode range)
    text = re.sub(r"[^\w\s,.\-–—:/]", " ", text)

    # 2. Normalize bullet points → comma
    text = re.sub(r"[•●▪︎]", ",", text)

    # 3. Normalize arrows
    text = text.replace("➡️", ",")

    # 4. Preserve dashes but normalize weird ones
    text = text.replace("–", "-").replace("—", "-")

    # 5. Collapse spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()