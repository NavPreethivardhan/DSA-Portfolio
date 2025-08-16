"""
Template: Breadth-First Search (Iterative)
Topic: Graphs/Trees
Difficulty: Template
"""

from collections import deque

def bfs(graph, start):
    """
    graph: dict of node -> list of neighbors
    returns list of visited nodes in BFS order
    """
    visited = set([start])
    order = []
    queue = deque([start])
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order

if __name__ == "__main__":
    graph = {0:[1,2],1:[2],2:[1],3:[]}
    print(bfs(graph, 0))  # Example BFS order
