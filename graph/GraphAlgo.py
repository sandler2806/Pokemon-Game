import cProfile
import logging
import math
from typing import List
import heapq as hp
from graph.DiGraph import DiGraph
from graph.Edge import Edge
from graph.GUI import draw
import json


class GraphAlgo:

    def __init__(self, g: DiGraph = None):
        if g is None:
            self.graph = DiGraph()
        else:
            self.graph = g

    def get_graph(self):
        """  :return: the directed graph on which the algorithm works on."""
        return self.graph

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
             """
        try:
            nodes = json.dumps(list(self.graph.get_all_v().values()), default=lambda o: o.__dict__, sort_keys=True,
                               indent=4)
            lstN = json.loads(nodes)
            for d in lstN:
                d["pos"] = str(d["pos"][0]) + "," + str(d["pos"][1]) + "," + str(d["pos"][2])
                del d["tag"]
                del d["inEdge"]
                del d["outEdge"]

            lstE = []
            for node in self.graph.get_all_v().values():
                for dest, edge in self.graph.all_out_edges_of_node(node.get__id()).items():
                    edge = Edge(node.get__id(), edge, dest)
                    lstE.append(edge)

            edges = json.dumps(lstE, default=lambda o: o.__dict__, sort_keys=True, indent=4)
            lstEd = json.loads(edges)

            dic = {"Edges": lstEd, "Nodes": lstN}
            s = json.dumps(dic, indent=4)

            with open(file_name, 'w') as f:
                f.write(s)
            return True

        except IOError as e:
            logging.exception(e)
            return False

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

    def load_from_json(self, file_name: str) -> bool:
        """
        Loads a graph from a json file.
        @param file_name: The path to the json file
        @returns True if the loading was successful, False o.w.
        """
        try:
            self.graph = DiGraph(file_name)

        except Exception as e:
            logging.exception(e)
            return False

        return True

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        """
        Finds the shortest path that visits all the nodes in the list
        :param node_lst: A list of nodes id's
        :return: A list of the nodes id's in the path, and the overall distance
        """
        minDist = math.inf
        minAns = []
        citisMap = {}
        dijkstraMap = {}
        # we construct several paths, each time starting from different node in cities
        for ind in node_lst:
            src = self.graph.get_node(ind)
            # we add all the cities to temp dictionary
            for n in node_lst:
                citisMap[n] = self.graph.get_node(n)
            dist = 0
            ans = [src]
            del citisMap[ind]
            # when we visit a city we remove it from the temp list
            while len(citisMap) > 0:
                minNei = None
                minWeight = math.inf
                # if we already performed dijkstra on the source then whe take the results
                if src.get__id() in dijkstraMap:
                    dijkstra = dijkstraMap[src.get__id()]
                else:
                    dijkstra = self.dijkstra(src.get__id())
                    dijkstraMap[src.get__id()] = dijkstra
                distance = dijkstra[1]
                path = dijkstra[0]
                # find the min neighbor from the list
                for nodeData in citisMap.values():
                    if distance[nodeData.get__id()] < minWeight:
                        minNei = nodeData
                        minWeight = distance[nodeData.get__id()]
                if minNei is None:
                    dist = math.inf
                    break
                # add the distance of the path between the nodes and create a path
                dist += distance[minNei.get__id()]
                ans.append(self.graph.get_node(minNei.get__id()))
                del citisMap[minNei.get__id()]
                node = path[minNei.get__id()]
                size = len(ans) - 1
                while node != src.get__id():
                    ans.insert(size, self.graph.get_node(int(node)))
                    if node in citisMap:
                        del citisMap[int(node)]
                    node = path[node]
                src = minNei
            # update the minimum dest and path
            if dist < minDist:
                minAns = ans
                minDist = dist
        # return the minimum path
        if minDist == math.inf:
            return None,math.inf

        ans = [x.id for x in minAns]
        return ans, minDist

    def centerPoint(self) -> (int, float):
        """
        Finds the node that has the shortest distance to it's farthest node.
        :return: The nodes id, min-maximum distance
        """
        # calculate the eccentricity of each node
        eccentricity = {}  # saving the eccentricity of each node
        for node in self.graph.get_all_v().values():
            distance = self.dijkstra(node.get__id())[1]
            max_value = max(distance.values())
            eccentricity[node.get__id()] = max_value
        # take the min value of all the eccentricity
        min_value = min(eccentricity.values())
        ind = list(eccentricity.keys())[list(eccentricity.values()).index(min_value)]

        Max = max(eccentricity.values())
        if Max == math.inf:  # one node is not reachable, there fore the graph is not connected
            ind=None
            min_value=math.inf
        # return the min eccentricity and the node index
        return ind, min_value

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """
        draw(self.graph)

    @staticmethod
    def getPath(prev: dict, src, dest):
        # create a path from source to destination by backtracking the prev dict(
        path = []
        while dest != src:
            path.insert(0, dest)
            dest = prev[dest]

        path.insert(0, src)

        return path

    def dijkstra(self, src: int) -> (dict, dict):
        # get the number of nodes from the graph
        nodes = self.graph.get_all_v()
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
                EdgesLst[k] = self.graph.adjList[k].outEdges.items()

        EdgesLst[src] = self.graph.adjList[src].outEdges.items()
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
