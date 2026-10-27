# program to create graph adjacency matrix

def add_edge(mat, i, j):
	mat[i][j]=1
	mat[j][i]=1

def display_matrix(mat):
	for row in mat:
		print(" ".join(map(str, row)))

if __name__=="__main__":
	v=4
	mat=[[0]*v for _ in range(v)]
	add_edge(mat, 0, 1)
	add_edge(mat, 0, 2)
	add_edge(mat, 1, 2)
	add_edge(mat, 2, 3)

	print("Adjacency matrix: ")
	display_matrix(mat)