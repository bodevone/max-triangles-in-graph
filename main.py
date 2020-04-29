from collections import defaultdict
import random
import math

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.k = 0
        self.v = 0
        self.e = 0
        self.vertices = []
        self.not_connected = []
        self.triangles_number = {}
        self.triangles = []
        self.solution1 = []
        self.solution2 = []
        self.solution3 = []
        self.s = []

    def generateGraph(self, v, e):
        self.v = v
        for i in range(v):
            if e > 0:
                if e > 5:
                    n = random.randint(1, 5)
                else:
                    n = random.randint(1, e)
                e -= n
                for j in range(n):
                    u = random.randint(0, v-1)
                    while u == i or u in self.graph[i]:
                        u = random.randint(0, v-1)

                    self.addEdge(i, u)

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)
        if u not in self.vertices:
            self.vertices.append(u)
        if v not in self.vertices:
            self.vertices.append(v)
        self.e += 1

    def setK(self, k):
        kMax = self.v*(self.v-1) / 2 - self.e
        print("Max value of k: " + str(kMax))
        if k > kMax:
            self.k = kMax
        else:
            self.k = k

    def printGraph(self):
        print("GRAPH")
        for key, value in self.graph.items():
            print(key, value)



    def solve1(self):
        self.findNotConnected()
        self.findTriangles()
        self.findKMaxTringles()
        print("Solution for i=1:")
        print(self.solution1)

    def findNotConnected(self):
        # Find edges which are not connected
        for node, neighbors in self.graph.items():
            for n in self.vertices:
                if n is not node and n not in neighbors:
                    temp_arr = [node, n]
                    temp_arr.sort()
                    if temp_arr not in self.not_connected:
                        self.not_connected.append(temp_arr)

    def findTriangles(self):
        # Find number of triangles for all unconnected vertices
        for i in range(len(self.not_connected)):
            self.find1(self.not_connected[i][0], self.not_connected[i][1], i)

    def find1(self, s, f, i):
        # Find number of triangles for given vertices
        for n1 in self.graph[s]:
            for n2 in self.graph[n1]:
                if s is n2:
                    name = str(s) + "-" + str(f)
                    if name in self.triangles_number:
                        self.triangles_number[name] += 1
                    else:
                        self.triangles_number[name] = 1

    def findKMaxTringles(self):
        # Find k shortcut edges with maximum number of triangles
        sorted_triangles = sorted(self.triangles_number, key=lambda x : self.triangles_number[x])[::-1]
        list_sorted_triangles = []
        for x in sorted_triangles:
            temp = x.split("-")
            list_sorted_triangles.append([int(temp[0]), int(temp[1])])

        if self.k > len(list_sorted_triangles):
            self.solution1 = list_sorted_triangles
        else:
            self.solution1 = list_sorted_triangles[:self.k]


    def solve3(self):
        k = self.findK()
        indepS = self.independetSet(k, 0)

        self.combineIndS(indepS)
        print("Solution for i=3:")
        print(self.solution3)

    def findK(self):
        # Find k (number of independent vertices) from our k
        # x**2 - x - 6*k = 0
        c = 6 * self.k
        D = math.sqrt(1 + 4*c)
        x1 = (1 + D) / 2
        return x1

    def independetSet(self, k, iter):
        # Randomly find Maximal Independent Set: set without adjacent vertices

        random_node = random.choice(self.vertices)
        available_nodes = set(self.vertices).difference(
            set([random_node]).union(set(self.graph[random_node])))
        indep_nodes = [random_node]
        while available_nodes:
            node = random.choice(list(available_nodes))
            indep_nodes.append(node)
            available_nodes = available_nodes.difference(
                set([node]).union(set(self.graph[node])))
        if len(indep_nodes) >= k or iter > 100:
            return indep_nodes
        else:
            return self.independetSet(k, iter+1)

    def combineIndS(self, indepS):
        for u in indepS:
            for v in indepS:
                if u != v and len(self.solution3) <= self.k:
                    temp = [u, v]
                    temp.sort()
                    if temp not in self.solution3:
                        self.solution3.append(temp)


    def solve2(self):
        self.findS()

        setI = self.algo2()
        self.solution2 = setI
        print("Solution for i=2:")
        print(self.solution2)

    def findS(self):
        # Find set S of vertices by taking random number <= k from G
        lenS = random.randint(1, self.k)
        self.s = self.vertices[:lenS]

    def algo2(self):
        # Implemenation of Algorithm 2
        mark = {}
        setI1 = []

        for n in self.vertices:
            mark[n] = False

        for u in self.vertices:
            if not mark[u] and u not in self.s and len(setI1) + len(self.s) <= self.k:
                mark[u] = True
                for v in self.s:
                    temp_arr = [u, v]
                    temp_arr.sort()
                    if temp_arr not in setI1:
                        setI1.append(temp_arr)

        if len(setI1) != len(self.s) * (len(self.vertices) - len(self.s)):
            return setI1

        k1 = self.k - len(setI1)
        setI2 = []

        for n in self.vertices:
            mark[n] = False

        vMax = self.s[0]

        for x in self.s[1:]:
            if len(self.graph[vMax]) < len(self.graph[x]):
                vMax = x

        freeNodes = len(self.s)

        for u in self.s:
            if u != vMax and not mark[u] and len(setI2) + freeNodes - 1 <= k1:
                mark[u] = True
                freeNodes -= 1
                for v in self.s:
                    if not mark[v]:
                        temp_arr = [u, v]
                        temp_arr.sort()
                        if temp_arr not in setI2:
                            setI2.append(temp_arr)
        if len(setI2) != (len(self.s)*(len(self.s)-1) / 2):
            return setI1 + setI2

        setI3 = []
        k2 = self.k - len(setI1) - len(setI2)

        for u in self.vertices:
            if u not in self.s and len(setI3) < k2:
                for v in self.vertices:
                    if v not in self.s and v != u and v not in self.graph[u]:
                        temp_arr = [u, v]
                        temp_arr.sort()
                        if temp_arr not in setI3:
                            setI3.append(temp_arr)

        return setI1 + setI2 + setI3


def example(graph):
    graph.addEdge(0, 1)
    graph.addEdge(0, 4)
    graph.addEdge(4, 3)
    graph.addEdge(2, 3)
    graph.addEdge(1, 2)
    graph.addEdge(1, 3)


if __name__ == "__main__":
    k = 10
    vertices = 10
    edges = 20

    graph = Graph()
    # example(graph)
    graph.generateGraph(vertices, edges)
    graph.setK(k)

    graph.printGraph()

    graph.solve1()
    graph.solve2()
    graph.solve3()
