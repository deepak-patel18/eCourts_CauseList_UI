# utils.py
import os
from datetime import datetime
import json

def ensure_dirs():
    os.makedirs("output", exist_ok=True)
    os.makedirs("downloads", exist_ok=True)
    os.makedirs("tmp", exist_ok=True)

def today_str():
    return datetime.now().strftime("%Y-%m-%d")

def save_json(obj, prefix="result"):
    ensure_dirs()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join("output", f"{prefix}_{ts}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return path

def safe_filename(s):
    return "".join(c for c in s if c.isalnum() or c in " .-_").rstrip()
