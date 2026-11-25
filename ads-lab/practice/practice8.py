# graph using adjacency matrix, undirected, weighted
from collections import deque


def add_edge(v, i, j, w):
    v[i][j], v[j][i] = w, w

def bfs(v, start):
    n = len(v)
    q = deque([start])
    vis = [False]*n
    vis[start] = True
    while q:
        a = q.popleft()
        print(a, end=" ")
        for b in range(n):
            if v[a][b]!=-1 and not vis[b]:
                vis[b] = True
                q.append(b)

def dfs(v, start, vis=None):
    if not vis:
        vis = [False]*len(v)
    vis[start] = True
    print(start, end=" ")
    for b in range(len(v)):
        if v[start][b]!=-1 and not vis[b]:
            vis[b] = True
            dfs(v, b, vis)


if __name__=="__main__":
    v = 7
    mat = [[-1]*v for _ in range(v)]
    add_edge(mat, 0, 1, 3)
    add_edge(mat, 0, 3, 2)
    add_edge(mat, 1, 2, 6)
    add_edge(mat, 1, 3, 1)
    add_edge(mat, 3, 4, 1)
    add_edge(mat, 4, 6, 2)
    add_edge(mat, 4, 5, 4)
    add_edge(mat, 5, 6, 4)

    for row in mat:
        print(row)

    bfs(mat, 0)

    print()

    dfs(mat, 0)

