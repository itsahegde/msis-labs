# graph implementation using adjacency list

def add_edge(ad, i, j):
	adj[i].append(j)
	adj[j].append(i)

def display_adj_list(adj):
	for i in range(len(adj)):
		print(f"{i}: ", end="")
		for j in adj[i]:
			print(j, end="->")
		print()

if __name__=="__main__":
	v=4
	adj = [[] for _ in range(v)]
	add_edge(adj, 0, 1)
	add_edge(adj, 0, 2)
	add_edge(adj, 1, 2)
	add_edge(adj, 2, 3)
	print("Adjacency list representation: ")
	display_adj_list(adj)