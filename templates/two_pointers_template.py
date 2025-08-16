"""
Template: Two Pointers
Topic: Arrays/Strings
Difficulty: Template
"""

def two_sum_sorted(arr, target):
    """
    Given sorted arr, return indices of two numbers adding to target.
    """
    left, right = 0, len(arr) - 1
    while left < right:
        s = arr[left] + arr[right]
        if s == target:
            return [left, right]
        elif s < target:
            left += 1
        else:
            right -= 1
    return []

if __name__ == "__main__":
    arr = [2,7,11,15]
    print(two_sum_sorted(arr, 9))  # Expected [0,1]
