"""
This class represents a node in a graph
Node has the following info:
id : integer that represents which node it is, every node has it's own id number
pos : list with 3 parameters that represents a geographic point on the globe
tag : integer that represents the current state of node (used for algorithms i.e. BFS)
inEdge: counter of in edges
outEdge counter of out edges
0 --> white, 1--> gray, 2--> black
"""


class Node(object):
    # constructor
    def __init__(self, _id: int, _pos: tuple = (-1, -1, 0.0)):
        self.id = _id
        self.pos = (float(_pos[0]), float(_pos[1]), float(_pos[2]))
        self.tag = 0
        self.inEdge = 0
        self.outEdge = 0

    # string of information
    def __str__(self):
        return f'{self.id}: |edges out| {self.outEdge} |edges in| {self.inEdge}'

    # string for inside the list information
    def __repr__(self):
        return f'{self.id}: |edges out| {self.outEdge} |edges in| {self.inEdge}'

    # getter method for id
    def get__id(self):
        return self.id

    # setter method for id
    def set__id(self, x):
        self.id = x

    # getter method for pos
    def get__pos(self):
        return self.pos

    # setter method for pos
    def set__pos(self, val):
        self.pos = val

    # getter method for tag
    def get__tag(self):
        return self.tag

    # setter method for tag
    def set__tag(self, t):
        if t < 0:
            raise ValueError("the tag is invalid")
        if t > 2:
            raise ValueError("the tag is invalid")
        self.tag = t
