"""
Template: Depth-First Search (Recursive)
Topic: Graphs/Trees
Difficulty: Template
"""

def dfs(graph, start, visited=None, result=None):
    """
    graph: dict of node -> list of neighbors
    returns list of visited nodes in DFS order
    """
    if visited is None:
        visited = set()
    if result is None:
        result = []
    visited.add(start)
    result.append(start)
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            dfs(graph, neighbor, visited, result)
    return result

if __name__ == "__main__":
    graph = {0:[1,2],1:[2],2:[1],3:[]}
    print(dfs(graph, 0))  # Example DFS order
