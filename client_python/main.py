import json
from types import SimpleNamespace
from GUI import *
import pygame
from client_python.client import Client
from graph.DiGraph import DiGraph
from client_python.algo import allocateAgent, dispatchAgents, allocateEdge, dijkstra
import client_python.config as cnf
import math as mt

client: Client


def main():
    global client
    moveCounter = 0
    clock = pygame.time.Clock()
    catchPokemon = False
    client = Client()
    client.start_connection(cnf.HOST, cnf.PORT)

    print(client.get_agents())

    # load the map to graph
    cnf.gameMap = DiGraph(client.get_graph())
    # dispach as much agents as possible
    dispatchAgents(client)
    cnf.edgeBank = cnf.gameMap.edgeToLinear()
    cnf.agents = json.loads(client.get_agents(),
                            object_hook=lambda d: SimpleNamespace(**d)).Agents
    cnf.agents = [agent.Agent for agent in cnf.agents]
    # assigning the starting Pokemon's
    for node in cnf.gameMap.nodes.values():
        cnf.dijkstra[node.id] = dijkstra(node.id)[1]
    assignNewPok()

    init_GUI()
    # start the game
    client.start()
    cnf.timeToEnd = float(client.time_to_end())
    starTime = cnf.timeToEnd
    flag = 1
    while flag:
        cnf.timeToEnd=float(client.time_to_end())

        if len(cnf.agentsPath[0]) == 0:
            print("")


        # assigning an agent for new pokemon's from the server
        # check if any of the agents need to 'Move'

        set_next_node()

        if len(cnf.moveTimes) == 0:
            print(client.time_to_end())
            print("")

        cnf.pokemonTimes.sort(reverse=True)
        if len(cnf.pokemonTimes) > 0 and cnf.pokemonTimes[0] >= cnf.timeToEnd:
            client.move()
            print(client.get_agents())
            print(client.get_info())
            print(client.time_to_end())
            print(cnf.agentsPath[0])
            print(cnf.pokemons)
            print("pop pokemon time: " + str(cnf.pokemonTimes.pop(0)))
        print("move time: "+str(cnf.moveTimes))
        timePassed = starTime - cnf.timeToEnd
        if catchPokemon or (False in cnf.isMoved and moveCounter <= timePassed / 100):
            cnf.moveTimes.sort(reverse=True)
            if len(cnf.moveTimes) > 0 and cnf.moveTimes[0] > cnf.timeToEnd:
                client.move()
                print("moved")
                moveCounter += 1
                cnf.isMoved = [True for _ in range(cnf.agentsNum)]
            while len(cnf.moveTimes) > 0 and cnf.moveTimes[0] > cnf.timeToEnd:
                print("pop move time: "+str(cnf.moveTimes.pop(0)))

            catchPokemon = False

        draw()
        assignNewPok()
        # client.move()
        clock.tick(60)

    # while True:
    #     print(client.get_agents())
    #     client.choose_next_edge('{"agent_id":' + str(0) + ', "next_node_id":' + str(8) + '}')
    #     client.move()
    #     print(client.get_agents())
    #     # print(client.get_agents())
    #     # print(client.get_agents())
    #
    #     client.move()
    #     print(client.get_agents())
    #     print(client.get_agents())
    #
    #     print(client.get_agents())
    #     print(client.get_agents())
    #     print(client.get_agents())
    #     print(client.get_agents())
    #
    #     # print(client.get_info())
    #     client.choose_next_edge('{"agent_id":' + str(0) + ', "next_node_id":' + str(9) + '}')
    #     print(client.get_agents())
    #     print(client.get_info())
    #     client.move()


# def init_game():
#     global client
#     client = Client()
#     client = Client()
#     client.start_connection(cnf.HOST, cnf.PORT)


def isHandled(pok) -> bool:
    for p in cnf.handledPokemons:
        if p.pos == pok.pos and p.type == pok.type:
            return True
    return False


def assignNewPok():
    cnf.pokemons = json.loads(client.get_pokemons(),
                              object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    cnf.pokemons = [p.Pokemon for p in cnf.pokemons]

    cnf.agents = json.loads(client.get_agents(),
                            object_hook=lambda d: SimpleNamespace(**d)).Agents
    cnf.agents = [agent.Agent for agent in cnf.agents]

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
            allocateAgent(pok)
            cnf.handledPokemons.append(pok)


def set_next_node():
    EPS = 0.001
    for i in range(cnf.agentsNum):
        if cnf.agents[i].dest == -1 and len(cnf.agentsPath[i]) and cnf.isMoved[i]:
            cnf.isMoved[i] = False
            src = cnf.agents[i].src
            Next = cnf.agentsPath[i].pop(0)
            # if Next % 1==0.75:
            #     client.move()
            #     Next = int(Next)
            if (src, Next) in cnf.criticalEdge[i]:
                cnf.criticalEdge[i].remove((src, Next))
                Next = int(Next)
                pokOnEdge = []
                for pokemon in cnf.pokemons:
                    x, y, _ = pokemon.pos.split(',')
                    edge = allocateEdge(cnf.edgeBank, [x, y], pokemon.type)
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
                    print("add pokemon time: "+str(cnf.timeToEnd - ((pokWeight / cnf.agents[i].speed) * 1000)))

            client.choose_next_edge('{"agent_id":' + str(i) + ', "next_node_id":' + str(Next) + '}')
            weight = cnf.gameMap.all_out_edges_of_node(src)[Next]
            cnf.moveTimes.append(cnf.timeToEnd - ((weight / cnf.agents[i].speed) * 1000))
            print("add move time: "+str(cnf.timeToEnd - ((weight / cnf.agents[i].speed) * 1000)))


if __name__ == "__main__":
    # init_game()
    main()
