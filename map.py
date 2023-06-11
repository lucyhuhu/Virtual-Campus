from cmu_112_graphics import *
import math
# This file creates a graph with vertices and edges. It also includes pathfinding
# functions that find the shortest path between two vertices and draw the path.


class Vertex():
    def __init__(self, name, cx, cy):
        self.name = name
        self.cx, self.cy = cx, cy
        self.r = 10
        self.neighbors = set()  # set of vertices

    def addNeighbor(self, other):
        self.neighbors.add(other)
        other.neighbors.add(self)


class Graph():
    vertices = dict()  # key is vertex name, val is the object vertex
    edges = list()  # list of tuples of two vertices

    def addVertex(self, vertex):
        if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
            self.vertices[vertex.name] = vertex
            return True
        return False

    def addEdge(self, vertex1, vertex2):
        if (isinstance(vertex1, Vertex) and isinstance(vertex2, Vertex) and
                vertex1.name in self.vertices and vertex2.name in self.vertices):
            vertex1.addNeighbor(vertex2)
            vertex2.addNeighbor(vertex1)
            self.edges.append((vertex1, vertex2))
            return True
        return False


# Pathfinder:


    def getDistance(self, vertex1, vertex2):
        if not (isinstance(vertex1, Vertex) and isinstance(vertex2, Vertex)):
            return None
        if not (vertex1 in vertex2.neighbors and vertex2 in vertex1.neighbors):
            return None  # only want distance between adjacent vertices
        if vertex1 == vertex2:
            return 0
        x0, y0 = vertex1.cx, vertex1.cy
        x1, y1 = vertex2.cx, vertex2.cy
        return ((x1-x0)**2+(y1-y0)**2)**0.5

    def findPath(self, start, end):  # return minPath={vertex:prev vertex}
        distanceDict = dict()  # key is node, val is d from start
        pathDict = dict()  # key is node, val is prev node
        unvisited = set()
        minPath = dict()
        dx, dy = end.cx-start.cx, end.cy-start.cy
        for name, vertex in self.vertices.items():
            dx1, dy1 = vertex.cx-start.cx, vertex.cy-start.cy
            if (dx1 > 0) == (dx > 0) and (dy1 > 0) == (dy > 0):  # same dir
                unvisited.add(vertex)  # need to be visited
            elif ((dx1 > 0) == (dx > 0) and dy1 == 0) or ((dy1 > 0) == (dy > 0) and dx1 == 0):
                unvisited.add(vertex)
        return self.findPathHelper(start, end, pathDict, unvisited, math.inf, minPath)[1]

    def findPathHelper(self, start, end, pathDict, unvisited, minDistance, minPath, currentDistance=0):
        if start == end and pathDict:  # BC
            if currentDistance < minDistance:
                return (currentDistance, pathDict.copy())
            return (minDistance, minPath)
        else:  # RC
            for neighbor in start.neighbors:
                if neighbor in unvisited:  # possible moves
                    if self.getDistance(start, neighbor) != None:  # valid move
                        currentDistance += self.getDistance(
                            start, neighbor)
                        if currentDistance < minDistance:
                            # update unvisited set
                            unvisited.remove(neighbor)

                            pathDict[neighbor] = start  # update path
                            solution = self.findPathHelper(neighbor, end,
                                                           pathDict, unvisited, minDistance, minPath, currentDistance)

                            if solution != None:
                                solutionDistance, solutionPath = solution
                                if currentDistance < minDistance:
                                    minDistance = solutionDistance
                                    minPath = solutionPath

                            unvisited.add(neighbor)
                            del pathDict[neighbor]
                            currentDistance -= self.getDistance(
                                start, neighbor)
            return (minDistance, minPath)

    def drawGraph(self, canvas):
        for edge in self.edges:  # draw edge
            (vertex1, vertex2) = edge
            canvas.create_line(vertex1.cx, vertex1.cy, vertex2.cx, vertex2.cy)
        for name, vertex in self.vertices.items():  # draw vertex
            canvas.create_oval(vertex.cx - vertex.r, vertex.cy - vertex.r,
                               vertex.cx + vertex.r, vertex.cy + vertex.r, fill='maroon')
            canvas.create_text(vertex.cx, vertex.cy, text=vertex.name,
                               font='Arial 8', fill='white')

    def drawPath(self, canvas, path):
        for vertex1, vertex2 in path.items():
            canvas.create_line(vertex1.cx, vertex1.cy, vertex2.cx,
                               vertex2.cy, fill='DarkSeaGreen4', width=5)


g = Graph()
tep = Vertex('TEP', 640, 180)
ghc = Vertex('GHC', 695, 376)
dh = Vertex('DH', 678, 513)
cuc = Vertex('CUC', 930, 403)
nsh = Vertex('NSH', 590, 406)
weh = Vertex('WEH', 588, 490)
bh = Vertex('BH', 640, 638)
cfa = Vertex('CFA', 845, 633)
cyh = Vertex('CYH', 745, 293)
hbh = Vertex('HBH', 595, 293)
hl = Vertex('HL', 760, 688)
mi = Vertex('MI', 74, 66)
ph = Vertex('PH', 518, 600)
pos = Vertex('POS', 913, 670)
wh = Vertex('WH', 822, 310)
cut = Vertex('Cut', 810, 498)

g.addVertex(tep)
g.addVertex(ghc)
g.addVertex(dh)
g.addVertex(cuc)
g.addVertex(nsh)
g.addVertex(weh)
g.addVertex(bh)
g.addVertex(cfa)
g.addVertex(cyh)
g.addVertex(hbh)
g.addVertex(hl)
g.addVertex(mi)
g.addVertex(ph)
g.addVertex(pos)
g.addVertex(wh)
g.addVertex(cut)

g.addEdge(tep, nsh)
g.addEdge(tep, ghc)
g.addEdge(tep, cuc)
g.addEdge(ghc, nsh)
g.addEdge(ghc, cuc)
g.addEdge(weh, nsh)
g.addEdge(weh, cuc)
g.addEdge(weh, dh)
g.addEdge(cuc, dh)
g.addEdge(mi, tep)
g.addEdge(mi, hbh)
g.addEdge(hbh, cyh)
g.addEdge(hbh, tep)
g.addEdge(hbh, ghc)
g.addEdge(hbh, nsh)
g.addEdge(tep, cyh)
g.addEdge(tep, wh)
g.addEdge(cyh, wh)
g.addEdge(cyh, ghc)
g.addEdge(cyh, cuc)
g.addEdge(cyh, wh)
g.addEdge(ghc, dh)
g.addEdge(cut, dh)
g.addEdge(cut, ghc)
g.addEdge(cut, cyh)
g.addEdge(cut, wh)
g.addEdge(cut, cuc)
g.addEdge(ph, weh)
g.addEdge(bh, dh)
g.addEdge(ph, bh)
g.addEdge(cfa, cut)
g.addEdge(pos, cut)
g.addEdge(hl, cut)
g.addEdge(hl, cfa)
g.addEdge(cfa, pos)
g.addEdge(hl, bh)
g.addEdge(pos, cuc)
g.addEdge(cut, bh)
g.addEdge(dh, cfa)
