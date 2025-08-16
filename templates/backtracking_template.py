"""
Template: Backtracking
Topic: Backtracking
Difficulty: Template
"""

def backtrack(path, choices, results):
    """
    Generic backtracking framework.
    path: current partial solution
    choices: list of possible next elements
    results: list to store complete solutions
    """
    if some_completion_condition(path):  # TODO: define completion check
        results.append(path.copy())
        return
    for choice in choices:
        # TODO: check if choice valid
        path.append(choice)
        backtrack(path, choices, results)
        path.pop()

# Example usage: Permutations
def permute(nums):
    results = []
    def helper(path):
        if len(path) == len(nums):
            results.append(path.copy())
            return
        for n in nums:
            if n in path:
                continue
            path.append(n)
            helper(path)
            path.pop()
    helper([])
    return results

def some_completion_condition(path):
    pass
    # Define your completion condition here

if __name__ == "__main__":
    print(permute([1,2,3]))  # Example permutations
