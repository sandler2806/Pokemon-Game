"""
This class represents an edge in a graph
Edge has the following info:
src : integer that represents the source node of the edge
w : float that represents the weight of the edge
dest : integer that represents the destination node of the edge
"""


class Edge(object):
    # constructor
    def __init__(self, src: int, w: float, dest: int):
        self.src = src
        self.w = w
        self.dest = dest

    # string of information
    def __str__(self):
        return f'Edge({self.src},{self.w},{self.dest})'

    # string
    def __repr__(self):
        return str(self)

    # getter method for src
    def get_src(self):
        return self.src

    # setter method for src
    def set_src(self, x):
        self.src = x

    # getter method for w
    def get_w(self):
        return self.w

    # setter method for w
    def set_w(self, x):
        if x < 0:
            raise ValueError("the weight is invalid")
        self.w = x

    # getter method for dest
    def get_dest(self):
        return self.dest

    # setter method for dest
    def set_dest(self, x):
        self.dest = x
