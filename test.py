# A Python3 program for finding number of
# triangles in an Undirected Graph. The
# program is for adjacency matrix
# representation of the graph

# Utility function for matrix
# multiplication
def multiply(A, B, C):
	global V
	for i in range(V):
		for j in range(V):
			C[i][j] = 0
			for k in range(V):
				C[i][j] += A[i][k] * B[k][j]

# Utility function to calculate
# trace of a matrix (sum of
# diagnonal elements)
def getTrace(graph):
	global V
	trace = 0
	for i in range(V):
		trace += graph[i][i]
	return trace

# Utility function for calculating
# number of triangles in graph
def triangleInGraph(graph):
	global V

	# To Store graph^2
	aux2 = [[None] * V for i in range(V)]

	# To Store graph^3
	aux3 = [[None] * V for i in range(V)]

	# Initialising aux
	# matrices with 0
	for i in range(V):
		for j in range(V):
			aux2[i][j] = aux3[i][j] = 0

	# aux2 is graph^2 now printMatrix(aux2)
	multiply(graph, graph, aux2)

	# after this multiplication aux3 is
	# graph^3 printMatrix(aux3)
	multiply(graph, aux2, aux3)

	trace = getTrace(aux3)
	return trace // 6

# Driver Code

# Number of vertices in the graph
V = 5
graph = [[0, 1, 0, 1, 0],
        [1, 0, 1, 1, 1],
        [0, 1, 0, 1, 1],
        [1, 1, 1, 0, 1],
        [1, 1, 1, 1, 0]]


print("Total number of Triangle in Graph :",
					triangleInGraph(graph))

# This code is contributed by PranchalK
