import math

from graph.DiGraph import DiGraph
from graph.GraphAlgo import GraphAlgo
from client_python.client import *
import json
from client_python.config import *
from types import SimpleNamespace
import heapq as hp




def alocateEdge(bank: dict[str, (float, float)], pos: list):
    x = pos[0]
    y = pos[1]

    for edge, mb in bank.items():
        m = mb[0]
        b = mb[1]
        booli = (float(y) == m * float(x) + b)
        if booli:
            return edge
    return None

def alocateAgent(pokemon:SimpleNamespace):
    delay=math.inf
    for agent in agents:
        if len(agentsPath[agent.id])==0:



def dispatchAgents():
    pass


def dijkstra(src: int) -> (dict, dict):
    # get the number of nodes from the graph
    nodes = gameMap.get_all_v()
    # create and initialize distance and prev dicts, we return these as the result
    distances = {}
    prev = {}
    # create a list that keep track of visited nodes
    visited = {}

    # and a queue based on heap
    que = []
    hp.heappush(que, (0, src))
    EdgesLst = {}
    for k, v in nodes.items():
        if k != src:
            visited[k] = False
            distances[k] = math.inf
            prev[k] = None
            EdgesLst[k] = gameMap.adjList[k].outEdges.items()

    EdgesLst[src] = gameMap.adjList[src].outEdges.items()
    distances[src] = 0
    prev[src] = src

    while len(que) > 0:
        # pop the smallest vertex
        dis, u = hp.heappop(que)
        visited[u] = True  # mark the node as visited

        # traverse U's neighbours
        edges = EdgesLst[u]
        for ID, w in edges:
            ID = int(ID)
            if not visited[ID]:
                altDis = dis + w  # compute the distance to U + dis(u,v)
                if altDis < distances[ID]:
                    distances[ID] = altDis
                    prev[ID] = u
                    hp.heappush(que, (altDis, ID))  # requeue v with the new priority

    return prev, distances

 def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through
        """
        # perform dijkstra on the source node and return the path and distance
        prev, distances = self.dijkstra(id1)
        if distances[id2] == math.inf:
            return math.inf, []
        return distances[id2], self.getPath(prev, id1, id2)