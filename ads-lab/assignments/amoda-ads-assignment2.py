
import math
from collections import deque

# graph build part

vertices = ['A', 'B', 'C', 'D', 'E', 'F']

edges = [
    ('A', 'B', 4),
    ('A', 'C', 2),
    ('B', 'C', 1),
    ('B', 'D', 5),
    ('C', 'D', 8),
    ('C', 'E', 10),
    ('D', 'E', 2),
    ('D', 'F', 6),
    ('E', 'F', 3)
]

# Build weighted adjacency list
graph = {v: {} for v in vertices}

for u, v, weight in edges:
    graph[u][v] = weight
    graph[v][u] = weight  # Undirected graph

# Sort adjacent vertices alphabetically
for v in vertices:
    graph[v] = dict(sorted(graph[v].items()))

print("ADJACENCY LIST")
for v in vertices:
    print(v, ":", graph[v])


# a Weighted adjacency matrix

matrix = []

for u in vertices:
    row = []
    for v in vertices:
        if u == v:
            row.append(0)
        elif v in graph[u]:
            row.append(graph[u][v])
        else:
            row.append(math.inf)
    matrix.append(row)

print("\nWEIGHTED ADJACENCY MATRIX")
print("    ", "  ".join(vertices))

for i, row in enumerate(matrix):
    values = [
        "∞" if x == math.inf else str(x)
        for x in row
    ]
    print(vertices[i], "  ", "  ".join(values))


# b BFS

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    order = []

    while queue:
        vertex = queue.popleft()
        order.append(vertex)

        for neighbour in graph[vertex]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)

    return order


# b DFS
def dfs(graph, start):
    visited = set()
    order = []

    def visit(vertex):
        visited.add(vertex)
        order.append(vertex)

        for neighbour in graph[vertex]:
            if neighbour not in visited:
                visit(neighbour)

    visit(start)
    return order


print("\nBREADTH-FIRST SEARCH")
print("BFS:", " -> ".join(bfs(graph, 'A')))

print("\nDEPTH-FIRST SEARCH")
print("DFS:", " -> ".join(dfs(graph, 'A')))

# c Dijikstra

def dijkstra(graph, start):
    distance = {v: math.inf for v in graph}
    predecessor = {v: None for v in graph}
    unvisited = set(graph)

    distance[start] = 0
    final_order = []

    while unvisited:
        # Select the unvisited vertex with
        # minimum distance; alphabetical tie-break
        u = min(unvisited, key=lambda v: (distance[v], v))

        if distance[u] == math.inf:
            break

        unvisited.remove(u)
        final_order.append(u)

        # Relax edges to unvisited neighbours
        for v, weight in graph[u].items():
            if v in unvisited:
                new_distance = distance[u] + weight

                if new_distance < distance[v]:
                    distance[v] = new_distance
                    predecessor[v] = u

        print(
            f"Finalized {u}: "
            f"distance = {distance[u]}, "
            f"predecessor = {predecessor[u]}"
        )

    return distance, predecessor, final_order


def shortest_path(predecessor, start, target):
    path = []
    current = target

    while current is not None:
        path.append(current)
        if current == start:
            break
        current = predecessor[current]

    path.reverse()

    if not path or path[0] != start:
        return []

    return path


print("\nDIJKSTRA'S ALGORITHM FROM A")

distances, predecessors, final_order = dijkstra(graph, 'A')

target = 'F'
path = shortest_path(predecessors, 'A', target)

print("\nShortest path from A to F:")
print(" -> ".join(path))
print("Total cost:", distances[target])


'''
OUTPUT:

ADJACENCY LIST
A : {'B': 4, 'C': 2}
B : {'A': 4, 'C': 1, 'D': 5}
C : {'A': 2, 'B': 1, 'D': 8, 'E': 10}
D : {'B': 5, 'C': 8, 'E': 2, 'F': 6}
E : {'C': 10, 'D': 2, 'F': 3}
F : {'D': 6, 'E': 3}

WEIGHTED ADJACENCY MATRIX
     A  B  C  D  E  F
A    0  4  2  ∞  ∞  ∞
B    4  0  1  5  ∞  ∞
C    2  1  0  8  10  ∞
D    ∞  5  8  0  2  6
E    ∞  ∞  10  2  0  3
F    ∞  ∞  ∞  6  3  0

BREADTH-FIRST SEARCH
BFS: A -> B -> C -> D -> E -> F

DEPTH-FIRST SEARCH
DFS: A -> B -> C -> D -> E -> F

DIJKSTRA'S ALGORITHM FROM A
Finalized A: distance = 0, predecessor = None
Finalized C: distance = 2, predecessor = A
Finalized B: distance = 3, predecessor = C
Finalized D: distance = 8, predecessor = B
Finalized E: distance = 10, predecessor = D
Finalized F: distance = 13, predecessor = E

Shortest path from A to F:
A -> C -> B -> D -> E -> F
Total cost: 13

time-comp: O((V + E) log V)
For this graph (V=6, E=9): O((6+9) log 6) = O(15 log 6)

'''