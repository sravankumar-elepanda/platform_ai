import json
import os

def load_assets(path):
    if not os.path.exists(path) or os.stat(path).st_size == 0:
        return {"Agents": [], "Scripts": [], "Workflows": [], "Platforms": []}
    with open(path) as f:
        return json.load(f)

def save_assets(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
