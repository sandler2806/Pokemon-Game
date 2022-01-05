import math
from numpy.linalg import norm
from client_python.client import *
import json
import client_python.config as cnf
from types import SimpleNamespace
import heapq as hp
import itertools
import copy
import numpy as np


class Algo:

    @staticmethod
    def allocateEdge(bank: dict[(float, float), (float, float)], pos: list, type: int) -> (float, float):
        x = float(pos[0])
        y = float(pos[1])
        pok = np.asarray([x, y])
        minDist = math.inf
        minEdge = []
        for edge, mb in bank.items():

            ps = (cnf.gameMap.nodes[edge[0]].pos[0], cnf.gameMap.nodes[edge[0]].pos[1])
            pd = (cnf.gameMap.nodes[edge[1]].pos[0], cnf.gameMap.nodes[edge[1]].pos[1])
            ps = np.asarray(ps)
            pd = np.asarray(pd)
            d = norm(np.cross(pd - ps, ps - pok)) / norm(pd - ps)
            if d < minDist:
                minDist = d
                minEdge = edge

        if type > 0:
            minEdge = (min(minEdge[0], minEdge[1]), max(minEdge[0], minEdge[1]))
        else:
            minEdge = (max(minEdge[0], minEdge[1]), min(minEdge[0], minEdge[1]))
        return minEdge

    @staticmethod
    def allocateAgent(pokemon: SimpleNamespace):
        minDelay = math.inf
        minAgent = None
        minPermute = []

        x, y, _ = pokemon.pos.split(',')
        newEdge = Algo.allocateEdge(cnf.edgeBank, [x, y], pokemon.type)

        for agent in cnf.agents:
            src = agent.src if agent.dest == -1 else agent.dest
            if len(cnf.agentsPath[agent.id]) == 0:
                dist = cnf.dijkstra[src][newEdge[0]]
                dist += cnf.gameMap.adjList[newEdge[0]].outEdges[newEdge[1]]
                if (dist / agent.speed) < minDelay:
                    minDelay = (dist / agent.speed)
                    minAgent = agent
            else:
                arriveNewPokemon = False
                pokemonEdges = list(copy.deepcopy(cnf.criticalEdge[agent.id]))
                if newEdge not in pokemonEdges:
                    pokemonEdges.insert(0, newEdge)
                else:
                    pokemonEdges.remove(newEdge)
                    pokemonEdges.insert(0, newEdge)
                permutes = list(itertools.permutations(list(range(0, len(pokemonEdges)))))

                for p in permutes:
                    dist = cnf.dijkstra[src][pokemonEdges[p[0]][0]]
                    dist += cnf.gameMap.adjList[pokemonEdges[p[0]][0]].outEdges[pokemonEdges[p[0]][1]]

                    for i in range(0, len(p) - 1):
                        if p[i] == 0:
                            arriveNewPokemon = True

                        edge = pokemonEdges[p[i]]
                        nextEdge = pokemonEdges[p[i + 1]]

                        dist += cnf.dijkstra[edge[1]][nextEdge[0]]
                        dist += cnf.gameMap.adjList[nextEdge[0]].outEdges[nextEdge[1]]

                        if not arriveNewPokemon:
                            dist += cnf.dijkstra[edge[1]][nextEdge[0]]
                            dist += cnf.gameMap.adjList[nextEdge[0]].outEdges[nextEdge[1]]

                    if dist / agent.speed < minDelay:
                        minDelay = dist / agent.speed
                        minAgent = agent
                        minPermute = p

        src = minAgent.src if minAgent.dest == -1 else minAgent.dest
        if len(cnf.criticalEdge[minAgent.id]) == 0:
            cnf.agentsPath[minAgent.id] = Algo.shortest_path(src, newEdge[0])[1]
            cnf.agentsPath[minAgent.id].append(newEdge[1])
            cnf.agentsPath[minAgent.id].pop(0)
            start = cnf.agentsPath[minAgent.id].pop(0)
            cnf.agentsPath[minAgent.id].insert(0, start)
        else:
            pokemonEdges = copy.deepcopy(cnf.criticalEdge[minAgent.id])
            if newEdge not in pokemonEdges:
                pokemonEdges.insert(0, newEdge)
            else:
                pokemonEdges.remove(newEdge)
                pokemonEdges.insert(0, newEdge)

            ans = []
            ans.extend(Algo.shortest_path(src, pokemonEdges[minPermute[0]][0])[1])
            ans.append(pokemonEdges[minPermute[0]][1])
            ans.pop(0)
            for i in range(0, len(minPermute) - 1):
                edge = pokemonEdges[minPermute[i]]
                nextEdge = pokemonEdges[minPermute[i + 1]]

                temp = Algo.shortest_path(edge[1], nextEdge[0])[1]
                temp.pop(0)
                ans.extend(temp)
                ans.append(nextEdge[1])
            cnf.agentsPath[minAgent.id] = ans
        if len(cnf.criticalEdge[minAgent.id]) == 0:
            cnf.criticalEdge[minAgent.id] = [newEdge]
        else:
            if newEdge not in cnf.criticalEdge[minAgent.id]:
                cnf.criticalEdge[minAgent.id].append(newEdge)

    @staticmethod
    def dijkstra(src: int) -> (dict, dict):
        # get the number of nodes from the graph

        nodes = cnf.gameMap.get_all_v()
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
                EdgesLst[k] = cnf.gameMap.adjList[k].outEdges.items()
        EdgesLst[src] = cnf.gameMap.adjList[src].outEdges.items()
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

    @staticmethod
    def shortest_path(id1: int, id2: int) -> (float, list):
        """
            Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
            @param id1: The start node id
            @param id2: The end node id
            @return: The distance of the path, a list of the nodes ids that the path goes through
            """
        # perform dijkstra on the source node and return the path and distance
        prev, distances = Algo.dijkstra(id1)
        if distances[id2] == math.inf:
            return math.inf, []
        return distances[id2], Algo.getPath(prev, id1, id2)

    @staticmethod
    def getPath(prev: dict, src, dest):
        # create a path from source to destination by backtracking the prev dict(
        path = []
        while dest != src:
            path.insert(0, dest)
            dest = prev[dest]

        path.insert(0, src)

        return path

    @staticmethod
    def dispatchAgents(c: Client):
        j = json.loads(c.get_info())
        cnf.agentsNum = j['GameServer']['agents']
        centerId = Algo.centerPoint()

        poks = copy.deepcopy(cnf.pokemons)
        agCounter = 0

        for i in range(0, len(poks)):
            if agCounter < cnf.agentsNum:
                edge = Algo.allocateEdge(cnf.edgeBank, poks[i].pos.split(','), poks[i].type)
                src = edge[0]
                str = "\"id\":{}".format(src)
                c.add_agent("{" + str + "}")
                cnf.is_on_way_to_pok.append([])
                cnf.isMoved.append(True)
                cnf.agentsPath[agCounter] = []
                cnf.criticalEdge[agCounter] = []
                agCounter += 1

        while agCounter < cnf.agentsNum:
            str = "\"id\":{}".format(centerId)
            c.add_agent("{" + str + "}")
            cnf.is_on_way_to_pok.append([])
            cnf.isMoved.append(True)
            cnf.agentsPath[agCounter] = []
            cnf.criticalEdge[agCounter] = []
            agCounter += 1

    @staticmethod
    def centerPoint() -> int:
        """
        Finds the node that has the shortest distance to it's farthest node.
        :return: The nodes id, min-maximum distance
        """
        # calculate the eccentricity of each node
        eccentricity = {}  # saving the eccentricity of each node
        for node in cnf.gameMap.get_all_v().values():
            distance = Algo.dijkstra(node.get__id())[1]
            max_value = max(distance.values())
            eccentricity[node.get__id()] = max_value
        # take the min value of all the eccentricity
        min_value = min(eccentricity.values())
        ind = list(eccentricity.keys())[list(eccentricity.values()).index(min_value)]

        Max = max(eccentricity.values())
        if Max == math.inf:  # one node is not reachable, there fore the graph is not connected
            ind = None
        # return the min eccentricity and the node index
        return ind
