# graph using adjacency list, undirected and weighted
from collections import defaultdict, deque


def add_edge(graph, i, j, w):
    graph[i].append((j, w))
    graph[j].append((i, w))

def bfs(v, start):
    q = deque([start])
    vis = {start}
    while q:
        a = q.popleft()
        print(a, end=" ")
        for (b, w) in graph[a]:
            if b not in vis:
                vis.add(b)
                q.append(b)

def dfs(v, start, vis=None):
    if not vis:
        vis = set()
    vis.add(start)
    print(start, end=" ")
    for (b, w) in graph[start]:
        if b not in vis:
            vis.add(b)
            dfs(v, b, vis)


if __name__=="__main__":
    n = 7
    graph = defaultdict(list)
    add_edge(graph, 0, 1, 3)
    add_edge(graph, 0, 3, 2)
    add_edge(graph, 1, 2, 6)
    add_edge(graph, 1, 3, 1)
    add_edge(graph, 3, 4, 1)
    add_edge(graph, 4, 6, 2)
    add_edge(graph, 4, 5, 4)

    for u in range(n):
        print(graph[u])

    bfs(graph, 0)

    print()

    dfs(graph, 0)

