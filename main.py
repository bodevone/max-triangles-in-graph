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

        self.choice = 0

    def generateGraph(self, v, e):
        # Generate random graph with v Vertices and e Edges
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
        self.v = len(self.vertices)

    def setK(self, k):
        kMax = int(self.v*(self.v-1) / 2 - self.e)
        print("Max value of k: " + str(kMax))
        if k > kMax:
            self.k = kMax
        else:
            self.k = k
        print(f"k: {self.k}")

    def printGraph(self):
        print("\nGRAPH")
        for key, value in self.graph.items():
            print(key, value)
        print()



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
                if n != node and n not in neighbors:
                    temp_arr = [node, n]
                    temp_arr.sort()
                    if temp_arr not in self.not_connected:
                        self.not_connected.append(temp_arr)

    def findTriangles(self):
        # Find number of triangles for all unconnected vertices
        for n in self.not_connected:
            self.find1(n[0], n[1])

    def find1(self, s, f):
        # Find number of triangles for given vertices
        name = str(s) + "-" + str(f)
        self.triangles_number[name] = 0

        for n in self.graph[s]:
            if f in self.graph[n]:
                if name in self.triangles_number:
                    self.triangles_number[name] += 1

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
        n = self.findN()
        self.arbitrarySet(n)

        print("Solution for i=3:")
        print(self.solution3)
        print()

    def findN(self):
        # Find number of vertices in C from our k
        # x** - x -2*k = 0
        c = 2 * self.k
        D = math.sqrt(1 + 4*c)
        x1 = (1 + D) / 2
        return int(x1)

    def arbitrarySet(self, n):
        # Select arbitrary set with n vertices and make k edges
        c = random.sample(self.vertices, max(3, n))
        for u in c:
            for v in c:
                if u != v:
                    temp = [u, v]
                    temp.sort()
                    if temp not in self.solution3:
                        self.solution3.append(temp)
        if len(self.solution3) > self.k:
            self.solution3 = self.solution3[:k]


    def solve2(self):
        self.findS()

        setI = self.algo2()
        self.solution2 = setI
        print("Solution for i=2:")
        print(self.solution2)

    def findS(self):
        # Find set S of vertices by taking random number <= k from G
        lenS = random.randint(1, self.k)
        # self.s = random.sample(self.vertices, min(k, self.v))
        self.s = random.sample(self.vertices, min(lenS, self.v))


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

    def findMaxTrianglesI(self):
        # Select I (1, 2 or 3) with the most number of triangles
        triangles1 = self.calculateTriangles(self.solution1)
        triangles2 = self.calculateTriangles(self.solution2)
        triangles3 = self.calculateTriangles(self.solution3)

        print(f"Number of triangles when i=1: {triangles1}")
        print(f"Number of triangles when i=2: {triangles2}")
        print(f"Number of triangles when i=3: {triangles3}")

        if triangles1 > triangles2 and triangles2 > triangles3:
            self.choice = 1
        elif triangles2 > triangles1 and triangles2 > triangles3:
            self.choice = 2
        else:
            self.choice = 3

        if self.choice == 1:
            print(f"Max triangles in i=1 with I: {self.solution1}")
        elif self.choice == 2:
            print(f"Max triangles in i=2 with I: {self.solution2}")
        else:
            print(f"Max triangles in i=3 with I: {self.solution3}")



    def calculateTriangles(self, setI):
        # Calculate number of triangles in G (V, E+I)
        triangles = 0
        trianglesSet = []

        for u in self.vertices:
            for v in self.vertices:
                for w in self.vertices:
                    if u != v and v != w:
                        temp1 = [u, v]
                        temp1.sort()
                        temp2 = [v, w]
                        temp2.sort()
                        temp3 = [u, w]
                        temp3.sort()

                        if (temp1 in setI or v in self.graph[u]) and \
                            (temp2 in setI or w in self.graph[v]) and \
                            (temp3 in setI or w in self.graph[u]):

                            tempTri = [u, v, w]
                            tempTri.sort()
                            if tempTri not in trianglesSet:
                                triangles += 1
                                trianglesSet.append(tempTri)
        return triangles


def example(graph):
    graph.addEdge(0, 1)
    graph.addEdge(1, 2)
    graph.addEdge(2, 3)
    graph.addEdge(3, 4)
    graph.addEdge(4, 5)
    graph.addEdge(5, 6)
    graph.addEdge(6, 7)
    graph.addEdge(7, 8)
    graph.addEdge(8, 0)


if __name__ == "__main__":
    # vertices = 10
    # edges = 20

    k = 18

    graph = Graph()
    example(graph)
    # graph.generateGraph(vertices, edges)
    graph.setK(k)

    graph.printGraph()

    graph.solve1()
    graph.solve2()
    graph.solve3()

    graph.findMaxTrianglesI()
