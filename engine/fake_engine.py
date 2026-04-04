import re
from engine.rules_loader import load_rules

def smart_fake(text):
    rules = load_rules()

    for word, replacement in rules.items():
        text = re.sub(rf"\b{word}\b", replacement, text, flags=re.IGNORECASE)

    return text