"""
Template: Graph Algorithms
Topic: Graphs
Difficulty: Template
"""

import heapq

def dijkstra(graph, source):
    """
    graph: dict node -> list of (neighbor, weight)
    returns shortest distances dict from source
    """
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    heap = [(0, source)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue
        for nei, w in graph[node]:
            nd = d + w
            if nd < dist[nei]:
                dist[nei] = nd
                heapq.heappush(heap, (nd, nei))
    return dist

if __name__ == "__main__":
    graph = {0:[(1,5),(2,1)],1:[(3,1)],2:[(1,2),(3,5)],3:[]}
    print(dijkstra(graph, 0))  # Expected shortest distances
