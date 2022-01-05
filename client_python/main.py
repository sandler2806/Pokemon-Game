import json
from GUI import *
import pygame
from client_python.client import Client
from graph.DiGraph import DiGraph
from client_python.algo import Algo
import client_python.config as cnf
import math as mt

client: Client

"""
The main function servers as the starting point of our app
it gets the data from the server and using to issue commands to other parts of the app
"""


def main():
    global client
    clock = pygame.time.Clock()
    cnf.client = client = Client()
    client.start_connection(cnf.HOST, cnf.PORT)

    # load the map to graph
    cnf.gameMap = DiGraph(client.get_graph())

    # update the edges from the graph in config
    cnf.edgeBank = cnf.gameMap.edgeToLinear()
    # loads the initial Pokemon's that appear in the game
    cnf.pokemons = json.loads(client.get_pokemons(),
                              object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    cnf.pokemons = [p.Pokemon for p in cnf.pokemons]

    # dispatch the maximum amount of agents on the game map
    Algo.dispatchAgents(client)
    cnf.agents = json.loads(client.get_agents(),
                            object_hook=lambda d: SimpleNamespace(**d)).Agents
    cnf.agents = [agent.Agent for agent in cnf.agents]

    # mapping the shortest path tables for each node in the graph (using dijkstra)
    for node in cnf.gameMap.nodes.values():
        cnf.dijkstra[node.id] = Algo.dijkstra(node.id)[1]

    # assigning the starting Pokemon's to agents
    assignNewPok()

    GUI.init_GUI()

    # start the game
    client.start()
    cnf.timeToEnd = float(client.time_to_end())
    starTime = cnf.timeToEnd

    flag = 1
    while flag:
        # get the current stats so we can print them on the screen
        info = json.loads(client.get_info())
        cnf.grade = info['GameServer']['grade']
        cnf.movecounter = info['GameServer']['moves']

        move = False
        cnf.timeToEnd = float(client.time_to_end())

        # assigning each agent it's next node destination
        set_next_node()

        # pokemonTimes keeps the times we need to catch pokemon's - sorted in descending order
        cnf.pokemonTimes.sort(reverse=True)

        # check if we need to catch pokemon now
        if len(cnf.pokemonTimes) > 0 and cnf.pokemonTimes[0] >= cnf.timeToEnd:
            move = True
            cnf.pokemonTimes.pop(0)

        timePassed = starTime - cnf.timeToEnd

        # check if we need to move an agent that reached a node
        if False in cnf.isMoved and cnf.movecounter <= timePassed / 100:
            cnf.moveTimes.sort(reverse=True, key=lambda y: y[0])

            if len(cnf.moveTimes) > 0 and cnf.moveTimes[0][0] > cnf.timeToEnd:
                move = True
            while len(cnf.moveTimes) > 0 and cnf.moveTimes[0][0] > cnf.timeToEnd:
                cnf.isMoved[cnf.moveTimes.pop(0)[1]] = True

        # if one of the condition above came true, we call move from the server
        if move:
            client.move()

        # update all the stats and drawing the GUI
        updateServer()
        GUI.draw()
        assignNewPok()
        clock.tick(60)


"""
check if a pokemon is already assigned an agent - necessary since we get all the
pokemon's currently active from the server, regardless of their assignment state
"""


def isHandled(pok) -> bool:
    for p in cnf.handledPokemons:
        if p.pos == pok.pos and p.type == pok.type:
            return True
    return False


"""
Assign a new pokemon to agent
"""


def assignNewPok():
    updateServer()

    for p in cnf.handledPokemons:
        exist = False
        for pok in cnf.pokemons:
            if p.pos == pok.pos and p.type == pok.type:
                exist = True
        if not exist:
            cnf.handledPokemons.remove(p)

    # look for new Pokemon's
    for pok in cnf.pokemons:
        if not isHandled(pok):
            Algo.allocateAgent(pok)
            cnf.handledPokemons.append(pok)


"""
Each agent has only source node and destination node, so we cant feed it it's full path.
for the we use this function to send him instructions one by one
"""


def set_next_node():
    for i in range(cnf.agentsNum):  # traverse the agents list
        if cnf.agents[i].dest == -1 and len(cnf.agentsPath[i]) and cnf.isMoved[i]:  # check if this agent has to move
            cnf.isMoved[i] = False
            src = cnf.agents[i].src
            Next = cnf.agentsPath[i].pop(0)

            if (src, Next) in cnf.criticalEdge[i]:  # check if we need to catch a pokemon on this edge
                cnf.criticalEdge[i].remove((src, Next))
                Next = int(Next)
                pokOnEdge = []
                for pokemon in cnf.pokemons:  # find the pokemon that "sit" on this edge
                    x, y, _ = pokemon.pos.split(',')
                    edge = Algo.allocateEdge(cnf.edgeBank, [x, y], pokemon.type)
                    if edge == (src, Next):
                        pokOnEdge.append(pokemon)

                weight = cnf.gameMap.all_out_edges_of_node(src)[Next]
                Sx, Sy, _ = cnf.agents[i].pos.split(',')
                Dx = cnf.gameMap.nodes[Next].pos[0]
                Dy = cnf.gameMap.nodes[Next].pos[1]
                edgeDistance = mt.sqrt(mt.pow(float(Sx) - Dx, 2) + mt.pow(float(Sy) - Dy, 2))

                for pokemon in pokOnEdge:  # calculate the catching time for the pokemon's on this edge
                    Px, Py, _ = pokemon.pos.split(',')
                    distance = mt.sqrt(mt.pow(float(Sx) - float(Px), 2) + mt.pow(float(Sy) - float(Py), 2))
                    pokWeight = (distance / edgeDistance) * weight
                    cnf.pokemonTimes.append(cnf.timeToEnd - ((pokWeight / cnf.agents[i].speed) * 1000))

            client.choose_next_edge('{"agent_id":' + str(i) + ', "next_node_id":' + str(Next) + '}')
            weight = cnf.gameMap.all_out_edges_of_node(src)[Next]
            cnf.moveTimes.append((float(client.time_to_end()) - ((weight / cnf.agents[i].speed) * 1000), i))


"""
Update the locations of pokemon's and agents currently on screen
"""


def updateServer():
    cnf.pokemons = json.loads(client.get_pokemons(),
                              object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    cnf.pokemons = [p.Pokemon for p in cnf.pokemons]

    cnf.agents = json.loads(client.get_agents(),
                            object_hook=lambda d: SimpleNamespace(**d)).Agents
    cnf.agents = [agent.Agent for agent in cnf.agents]


if __name__ == "__main__":
    main()
