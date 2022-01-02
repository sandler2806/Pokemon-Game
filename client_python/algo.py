import math

from graph.DiGraph import DiGraph
from graph.GraphAlgo import GraphAlgo
from client_python.client import *
import json
import client_python.config as cnf
from types import SimpleNamespace
import heapq as hp
import itertools
import copy


def allocateEdge(bank: dict[(float, float), (float, float)], pos: list) -> (float, float):
    x = pos[0]
    y = pos[1]

    for edge, mb in bank.items():
        m = mb[0]
        b = mb[1]
        booli = (float(y) == m * float(x) + b)
        if booli:
            return edge
    return None


def allocateAgent(pokemon: SimpleNamespace):
    minDelay = math.inf
    minAgent = None
    minPermute = []
    x, y, _ = pokemon.pos.split(',')
    newEdge = allocateEdge(cnf.edgeBank, [x, y])
    for agent in cnf.agents:
        src = agent.src if agent.dest == -1 else agent.dest
        if len(cnf.agentsPath[agent.id]) == 0:
            dist = shortest_path(src, newEdge[0])[0]
            dist += cnf.gameMap.adjList[newEdge[0]].outEdges[newEdge[1]]
            if dist / agent.speed < minDelay:
                minDelay = dist / agent.speed
                minAgent = agent.id
        else:
            arriveNewPokemon = False
            pokemonEdges = list(copy.deepcopy(cnf.criticalEdge[agent.id]))
            pokemonEdges.insert(0, newEdge)
            permutes = list(itertools.permutations(list(range(0, len(pokemonEdges)))))

            for p in permutes:
                dist = shortest_path(src, pokemonEdges[p[0]][0])[0]
                dist += cnf.gameMap.adjList[pokemonEdges[p[0]][0]].outEdges[pokemonEdges[p[0]][1]]

                for i in range(0, len(p) - 1):
                    if p[i] == 0:
                        arriveNewPokemon = True

                    edge = pokemonEdges[p[i]]
                    nextEdge = pokemonEdges[p[i + 1]]

                    dist += shortest_path(edge[1], nextEdge[0])[0]
                    dist += cnf.gameMap.adjList[nextEdge[0]].outEdges[nextEdge[1]]

                    if not arriveNewPokemon:
                        dist += shortest_path(edge[1], nextEdge[0])[0]
                        dist += cnf.gameMap.adjList[nextEdge[0]].outEdges[nextEdge[1]]

                if dist / agent.speed < minDelay:
                    minDelay = dist / agent.speed
                    minAgent = agent
                    minPermute = p
    if len(minPermute) == 0:
        cnf.agentsPath[minAgent.id] = shortest_path(minAgent.src, newEdge[0])[1]
        cnf.agentsPath[minAgent.id].append(newEdge[1] + 0.5)
    else:
        pokemonEdges = cnf.criticalEdge[minAgent.id]
        pokemonEdges.insert(0, newEdge)
        ans = []
        ans.extend(shortest_path(minAgent.src, pokemonEdges[minPermute[0]][0])[1])
        ans.append(pokemonEdges[minPermute[0]][1])
        ans.remove(0)
        for i in range(0, len(minPermute) - 1):
            edge = pokemonEdges[minPermute[i]]
            nextEdge = pokemonEdges[minPermute[i + 1]]

            ans.extend(shortest_path(edge[1], nextEdge[0])[1])
            ans.append(cnf.gameMap.adjList[nextEdge[0]].outEdges[nextEdge[1]])


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
    sdf = 4
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


def shortest_path(id1: int, id2: int) -> (float, list):
    """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through
        """
    # perform dijkstra on the source node and return the path and distance
    prev, distances = dijkstra(id1)
    if distances[id2] == math.inf:
        return math.inf, []
    return distances[id2], getPath(prev, id1, id2)


def getPath(prev: dict, src, dest):
    # create a path from source to destination by backtracking the prev dict(
    path = []
    while dest != src:
        path.insert(0, dest)
        dest = prev[dest]

    path.insert(0, src)

    return path


def dispatchAgents(c: Client):
    j = json.loads(c.get_info())
    cnf.agentsNum = j['GameServer']['agents']

    for i in range(0, cnf.agentsNum):
        str = "\"id\":{}".format(i)
        print(str)
        c.add_agent("{" + str + "}")
        cnf.is_on_way_to_pok.append(False)
