import csv
import json
import hashlib
from pathlib import Path

def encode(value):
    """Convert any value into a stable integer"""
    return int(hashlib.sha256(str(value).encode()).hexdigest(), 16)

def load_text(path, max_rows=None):
    data = []
    with open(path, encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f):
            if max_rows and i >= max_rows:
                break
            data.append(encode(line.strip()))
    return data

def load_csv(path, column=0, max_rows=None):
    data = []
    with open(path, newline="", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if max_rows and i >= max_rows:
                break
            if len(row) > column:
                data.append(encode(row[column]))
    return data

def load_json(path, key=None, max_rows=None):
    data = []
    with open(path, encoding="utf-8", errors="ignore") as f:
        records = json.load(f)
        for i, item in enumerate(records):
            if max_rows and i >= max_rows:
                break
            value = item[key] if key else item
            data.append(encode(value))
    return data

def load_any(path, **kwargs):
    ext = Path(path).suffix.lower()

    if ext in [".txt", ".log"]:
        return load_text(path, **kwargs)
    elif ext == ".csv":
        return load_csv(path, **kwargs)
    elif ext == ".json":
        return load_json(path, **kwargs)
    else:
        raise ValueError(f"Unsupported dataset type: {ext}")
