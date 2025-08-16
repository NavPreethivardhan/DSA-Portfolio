"""
Template: Union-Find (Disjoint Set Union)
Topic: Graphs/Union-Find
Difficulty: Template
"""

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0]*n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True

if __name__ == "__main__":
    uf = UnionFind(5)
    uf.union(0,1)
    uf.union(1,2)
    print(uf.find(2))  # Expected 0
