"""
Template: Sliding Window
Topic: Arrays/Strings
Difficulty: Template
"""

from collections import deque

def sliding_window_max(nums, k):
    """
    Returns list of max in each sliding window of size k.
    """
    if not nums or k == 0:
        return []
    result = []
    dq = deque()  # stores indices
    for i, n in enumerate(nums):
        # Remove indices out of current window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        # Remove smaller values than current
        while dq and nums[dq[-1]] < n:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result

if __name__ == "__main__":
    nums = [1,3,-1,-3,5,3,6,7]
    k = 3
    print(sliding_window_max(nums, k))  # Expected [3,3,5,5,6,7]
