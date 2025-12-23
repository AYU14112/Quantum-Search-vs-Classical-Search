# generate_dataset.py (optional helper)
with open("big_dataset.txt", "w") as f:
    for i in range(200000):
        f.write(f"Real world log entry number {i}\n")
