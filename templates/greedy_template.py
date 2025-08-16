"""
Template: Greedy Algorithms
Topic: Greedy
Difficulty: Template
"""

def greedy_template(items, key=lambda x: x):
    """
    Generic greedy selection framework.
    items: iterable of items
    key: sorting key function
    """
    sorted_items = sorted(items, key=key)
    result = []
    for item in sorted_items:
        # TODO: check if item can be selected
        result.append(item)
    return result

if __name__ == "__main__":
    # Example: Activity Selection
    activities = [(1,2),(3,4),(0,6),(5,7)]
    # greedy by finish time
    print(greedy_template(activities, key=lambda x: x[1]))
