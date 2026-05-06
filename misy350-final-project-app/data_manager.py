import json

def load_inventory(json_path):
    if json_path.exists():
        with open(json_path, "r") as f:
            return json.load(f)
    return []

def save_inventory(inventory, json_path):
    with open(json_path, "w") as f:
        json.dump(inventory, f, indent=4)