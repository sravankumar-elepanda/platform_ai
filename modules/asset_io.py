import os
import json

def load_assets(assets_file='data/assets.json'):
    if not os.path.exists(assets_file) or os.stat(assets_file).st_size == 0:
        return {"Agents": [], "Scripts": [], "Workflows": [], "Platforms": []}
    with open(assets_file) as f:
        return json.load(f)

def save_assets(data, assets_file='data/assets.json'):
    with open(assets_file, "w") as f:
        json.dump(data, f, indent=2)

