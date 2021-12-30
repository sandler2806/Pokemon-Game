import json
from abc import ABC


from graph.Node import Node


class Container:
    def __init__(self, node):
        self.node = node
        self.outEdges = {}
        self.inEdges = {}


class DiGraph:

    def __init__(self, file_name=""):
        self.mc = 0
        adjList = {}
        nodes = {}
        if file_name != "":
            with open(file_name, "r") as f:
                dict2 = json.load(f)
            edgesL = list(dict2.get('Edges'))
            nodesL = list(dict2.get('Nodes'))

            for nodeData in nodesL:
                nodeDataD = dict(nodeData)
                n_id = nodeDataD["id"]
                if "pos" in nodeDataD:
                    list_pos = list(nodeDataD["pos"].split(","))
                    node = Node(n_id, (list_pos[0], list_pos[1], list_pos[2]))
                else:
                    node = Node(n_id)
                adjList[n_id] = Container(node)
                nodes[n_id] = node

            for edgeData in edgesL:
                edgeDataD = dict(edgeData)
                src = edgeDataD["src"]
                dest = edgeDataD["dest"]
                weight = edgeDataD["w"]
                adjList[src].outEdges[dest] = weight
                adjList[dest].inEdges[src] = weight
                nodes[src].outEdge += 1
                nodes[dest].inEdge += 1

        self.adjList = adjList
        self.nodes = nodes

    def __str__(self):
        return f'Graph: |V|={self.v_size()} , |E|={self.e_size()}'

    def get_node(self, node_id):
        if node_id not in self.nodes:
            return
        return self.nodes[node_id]

    def v_size(self) -> int:
        return len(self.nodes)

    def e_size(self) -> int:
        size = 0
        for container in self.adjList.values():
            size += len(container.outEdges)

        return size

    def get_all_v(self) -> dict:
        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        return self.adjList[id1].inEdges

    def all_out_edges_of_node(self, id1: int) -> dict:
        return self.adjList[id1].outEdges

    def get_mc(self) -> int:
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 in self.nodes and id2 in self.nodes and id2 not in self.adjList[id1].outEdges:
            self.adjList[id1].outEdges[id2] = weight
            self.adjList[id2].inEdges[id1] = weight
            self.mc += 1
            self.nodes[id1].outEdge += 1
            self.nodes[id2].inEdge += 1
            return True

        return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id not in self.nodes:
            if pos is None:
                node = Node(node_id)
            else:
                if len(pos) == 2:
                    node = Node(node_id, (pos[0], pos[1], 0.0))
                else:
                    node = Node(node_id, (pos[0], pos[1], pos[2]))
            self.adjList[node_id] = Container(node)
            self.nodes[node_id] = node
            self.mc += 1
            return True

        return False

    def remove_node(self, node_id: int) -> bool:
        if node_id in self.nodes:
            outE = list(self.adjList[node_id].outEdges.keys())
            inE = list(self.adjList[node_id].inEdges.keys())
            for i in outE:
                self.remove_edge(node_id, i)
            for i in inE:
                self.remove_edge(i, node_id)

            del self.adjList[node_id]
            del self.nodes[node_id]
            self.mc += 1
            return True
        return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 in self.nodes and node_id2 in self.adjList[node_id1].outEdges:
            del self.adjList[node_id1].outEdges[node_id2]
            del self.adjList[node_id2].inEdges[node_id1]
            self.mc += 1
            self.nodes[node_id1].outEdge -= 1
            self.nodes[node_id2].inEdge -= 1
            return True
        return False
