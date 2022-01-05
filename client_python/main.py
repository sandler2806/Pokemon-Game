import json
from GUI import *
import pygame
from client_python.client import Client
from graph.DiGraph import DiGraph
from client_python.algo import Algo
import client_python.config as cnf
import math as mt

client: Client


def main():
    global client
    clock = pygame.time.Clock()
    cnf.client = client = Client()
    client.start_connection(cnf.HOST, cnf.PORT)

    # load the map to graph
    cnf.gameMap = DiGraph(client.get_graph())
    # dispatch as much agents as possible
    cnf.edgeBank = cnf.gameMap.edgeToLinear()
    cnf.pokemons = json.loads(client.get_pokemons(),
                              object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    cnf.pokemons = [p.Pokemon for p in cnf.pokemons]
    Algo.dispatchAgents(client)
    cnf.agents = json.loads(client.get_agents(),
                            object_hook=lambda d: SimpleNamespace(**d)).Agents
    cnf.agents = [agent.Agent for agent in cnf.agents]
    # assigning the starting Pokemon's
    for node in cnf.gameMap.nodes.values():
        cnf.dijkstra[node.id] = Algo.dijkstra(node.id)[1]
    assignNewPok()

    GUI.init_GUI()
    # start the game
    client.start()
    cnf.timeToEnd = float(client.time_to_end())
    starTime = cnf.timeToEnd
    flag = 1
    while flag:
        info = json.loads(client.get_info())
        cnf.grade = info['GameServer']['grade']
        cnf.movecounter = info['GameServer']['moves']
        move = False
        cnf.timeToEnd = float(client.time_to_end())
        # assigning an agent for new pokemon's from the server
        # check if any of the agents need to 'Move'

        set_next_node()

        cnf.pokemonTimes.sort(reverse=True)
        if len(cnf.pokemonTimes) > 0 and cnf.pokemonTimes[0] >= cnf.timeToEnd:
            move = True
            cnf.pokemonTimes.pop(0)

        timePassed = starTime - cnf.timeToEnd
        if False in cnf.isMoved and cnf.movecounter <= timePassed / 100:
            cnf.moveTimes.sort(reverse=True, key=lambda y: y[0])

            if len(cnf.moveTimes) > 0 and cnf.moveTimes[0][0] > cnf.timeToEnd:
                move = True
            while len(cnf.moveTimes) > 0 and cnf.moveTimes[0][0] > cnf.timeToEnd:
                cnf.isMoved[cnf.moveTimes.pop(0)[1]] = True

        if move:
            client.move()

        updateServer()
        GUI.draw()
        assignNewPok()
        clock.tick(60)


def isHandled(pok) -> bool:
    for p in cnf.handledPokemons:
        if p.pos == pok.pos and p.type == pok.type:
            return True
    return False


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


def set_next_node():
    for i in range(cnf.agentsNum):
        if cnf.agents[i].dest == -1 and len(cnf.agentsPath[i]) and cnf.isMoved[i]:
            cnf.isMoved[i] = False
            src = cnf.agents[i].src
            Next = cnf.agentsPath[i].pop(0)

            if (src, Next) in cnf.criticalEdge[i]:
                cnf.criticalEdge[i].remove((src, Next))
                Next = int(Next)
                pokOnEdge = []
                for pokemon in cnf.pokemons:
                    x, y, _ = pokemon.pos.split(',')
                    edge = Algo.allocateEdge(cnf.edgeBank, [x, y], pokemon.type)
                    if edge == (src, Next):
                        pokOnEdge.append(pokemon)

                weight = cnf.gameMap.all_out_edges_of_node(src)[Next]
                Sx, Sy, _ = cnf.agents[i].pos.split(',')
                Dx = cnf.gameMap.nodes[Next].pos[0]
                Dy = cnf.gameMap.nodes[Next].pos[1]
                edgeDistance = mt.sqrt(mt.pow(float(Sx) - Dx, 2) + mt.pow(float(Sy) - Dy, 2))

                for pokemon in pokOnEdge:
                    Px, Py, _ = pokemon.pos.split(',')
                    distance = mt.sqrt(mt.pow(float(Sx) - float(Px), 2) + mt.pow(float(Sy) - float(Py), 2))
                    pokWeight = (distance / edgeDistance) * weight
                    cnf.pokemonTimes.append(cnf.timeToEnd - ((pokWeight / cnf.agents[i].speed) * 1000))

            client.choose_next_edge('{"agent_id":' + str(i) + ', "next_node_id":' + str(Next) + '}')
            weight = cnf.gameMap.all_out_edges_of_node(src)[Next]
            cnf.moveTimes.append((float(client.time_to_end()) - ((weight / cnf.agents[i].speed) * 1000), i))


def updateServer():
    cnf.pokemons = json.loads(client.get_pokemons(),
                              object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    cnf.pokemons = [p.Pokemon for p in cnf.pokemons]

    cnf.agents = json.loads(client.get_agents(),
                            object_hook=lambda d: SimpleNamespace(**d)).Agents
    cnf.agents = [agent.Agent for agent in cnf.agents]


if __name__ == "__main__":
    main()
