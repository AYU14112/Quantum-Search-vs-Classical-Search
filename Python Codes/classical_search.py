# classical_search.py

def classical_search(dataset, target):
    """
    Performs linear search on a dataset.

    Parameters:
        dataset (list): List of items to search
        target (str/int): Target item to find

    Returns:
        index (int): Index of the target in the dataset (-1 if not found)
        steps (int): Number of steps taken
    """
    steps = 0
    for index, item in enumerate(dataset):
        steps += 1
        if item == target:
            return index, steps
    return -1, steps

# Example usage
if __name__ == "__main__":
    dataset = ['000', '001', '010', '011', '100', '101', '110', '111']
    target = '101'
    index, steps = classical_search(dataset, target)
    print(f"Target found at index {index} in {steps} steps")
