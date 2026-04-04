import json

def load_rules():
    with open("config/rules.json", "r") as f:
        return json.load(f)