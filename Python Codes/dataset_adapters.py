# dataset_adapters.py
import csv
import json
import hashlib
from pathlib import Path


def encode(value):
    """
    Encode any value into a stable integer using SHA-256.
    """
    return int(hashlib.sha256(str(value).encode()).hexdigest(), 16)


def load_and_find_target(path, target, max_rows=None):
    """
    Loads a dataset and finds the FIRST record that contains the target string.

    Supported formats:
      - .txt, .log  (line-based)
      - .csv        (row-based, all columns joined)
      - .json       (list of objects)

    Returns:
      dataset        -> list[int]   (encoded records)
      target_value   -> int         (encoded matched record)
      target_index   -> int         (index of matched record)
      matched_row    -> str / obj   (actual matched record)
    """

    ext = Path(path).suffix.lower()
    dataset = []
    target_value = None
    target_index = None
    matched_row = None
    target_lower = target.lower()

    def check_and_add(record):
        nonlocal target_value, target_index, matched_row
        encoded = encode(record)
        dataset.append(encoded)

        if target_index is None and target_lower in str(record).lower():
            target_value = encoded
            target_index = len(dataset) - 1
            matched_row = record

    # ---------- TXT / LOG ----------
    if ext in [".txt", ".log"]:
        with open(path, encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f):
                if max_rows and i >= max_rows:
                    break
                line = line.strip()
                if line:
                    check_and_add(line)

    # ---------- CSV ----------
    elif ext == ".csv":
        with open(path, newline="", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if max_rows and i >= max_rows:
                    break
                joined_row = " ".join(row)
                check_and_add(joined_row)

    # ---------- JSON ----------
    elif ext == ".json":
        with open(path, encoding="utf-8", errors="ignore") as f:
            records = json.load(f)
            if not isinstance(records, list):
                raise ValueError("JSON file must contain a list of records")

            for i, item in enumerate(records):
                if max_rows and i >= max_rows:
                    break
                check_and_add(item)

    else:
        raise ValueError(f"Unsupported dataset type: {ext}")

    if target_index is None:
        raise ValueError("Target not found in dataset")

    return dataset, target_value, target_index, matched_row
