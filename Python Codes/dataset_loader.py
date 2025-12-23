# dataset_loader.py
import hashlib
import random

def text_to_int(text: str) -> int:
    """Convert arbitrary text to a large integer using SHA-256"""
    return int(hashlib.sha256(text.encode()).hexdigest(), 16)

def load_dataset_from_file(file_path: str, max_lines=None):
    """
    Loads a dataset from a file.
    Each line becomes one data entry.
    """
    dataset = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f):
            if max_lines and i >= max_lines:
                break
            clean = line.strip()
            if clean:
                dataset.append(text_to_int(clean))
    return dataset

def sample_window(dataset, size):
    """Randomly sample a window of size 2^n"""
    if size > len(dataset):
        raise ValueError("Dataset smaller than requested quantum window size.")
    return random.sample(dataset, size)
