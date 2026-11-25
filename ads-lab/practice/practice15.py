import heapq


def prim(graph, start):
    vis = set()
    mst = []
    total = 0

    heap = [(0, start, start)]
    #vis.add(start)

    while heap:
        w, u, v = heapq.heappop(heap)
        if v in vis:
            continue
        vis.add(v)
        if u!=v:
            mst.append((u, v, w))
            total+=w
        for (nb, nw) in graph[v]:
            if nb not in vis:
                heapq.heappush(heap, (nw, v, nb))
    return mst, total

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

    mst, total = prim(graph, 0)
    print("Prims")
    print(mst)
    print(total)

