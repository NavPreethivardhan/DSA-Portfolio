"""
Template: Binary Search
Topic: Arrays/Strings
Difficulty: Template
"""

def binary_search(arr, target):
    """
    Binary search for target in sorted arr.
    Returns index or -1 if not found.
    """
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

if __name__ == "__main__":
    # Example test
    arr = [1, 2, 3, 4, 5]
    print(binary_search(arr, 3))  # Expected 2
