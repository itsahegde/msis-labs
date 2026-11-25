# dijkstra

import heapq


def dijkstra(graph, start):
    dist = {v: float('inf') for v in graph}
    prev = {v: None for v in graph}
    dist[start] = 0
    heap = [(0, start)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for (v, w) in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    return dist, prev


# graph using adjacency list, undirected and weighted
from collections import defaultdict


def add_edge(graph, i, j, w):
    graph[i].append((j, w))
    graph[j].append((i, w))

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

    dist, prev = dijkstra(graph, 0)
    print("Dijkstra")
    print(dist)
    print(prev)

