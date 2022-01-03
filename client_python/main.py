import json
from types import SimpleNamespace
from GUI import *
import pygame
from client_python.client import Client
from graph.DiGraph import DiGraph
from client_python.algo import allocateAgent, dispatchAgents, allocateEdge
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
    # assigning the starting Pokemon's
    assignNewPok()

    init_GUI()
    # start the game
    client.start()
    starTime = float(client.time_to_end())
    flag = 1
    while flag:
        print(client.get_agents())
        print(client.get_info())
        print(client.time_to_end())
        # assigning an agent for new pokemon's from the server
        # check if any of the agents need to 'Move'

        set_next_node()

        # print(agentsStatus)
        # for agent in cnf.agents:
        #     if len(cnf.is_on_way_to_pok[agent.id]) != 0:
        #         for pos in cnf.is_on_way_to_pok[agent.id]:
        #             x, y, _ = agent.pos.split(',')
        #             if abs(pos[0] - x) < EPS and abs(pos[1] - y) < EPS:
        #                 catchPokemon = True
        #                 cnf.is_on_way_to_pok[agent.id].remove(pos)
        cnf.pokemonTimes.sort(reverse=True)
        if len(cnf.pokemonTimes) > 0 and cnf.pokemonTimes[0] >= float(client.time_to_end()):
            client.move()
            print("ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp")
            cnf.pokemonTimes.pop(0)

        timePassed = starTime - float(client.time_to_end())
        print(catchPokemon)
        print(False in cnf.isMoved)
        if catchPokemon or (False in cnf.isMoved and moveCounter <= timePassed / 100):
            cnf.moveTimes.sort(reverse=True)
            if len(cnf.moveTimes) > 0 and cnf.moveTimes[0] >= float(client.time_to_end()):
                client.move()
                print("moved")
                moveCounter += 1
                cnf.isMoved = [True for _ in range(cnf.agentsNum)]
            while len(cnf.moveTimes) > 0 and cnf.moveTimes[0] >= float(client.time_to_end()):
                cnf.moveTimes.pop(0)

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
                    cnf.pokemonTimes.append(float(client.time_to_end()) - ((pokWeight / cnf.agents[i].speed) * 1000))

            client.choose_next_edge('{"agent_id":' + str(i) + ', "next_node_id":' + str(Next) + '}')
            weight = cnf.gameMap.all_out_edges_of_node(src)[Next]
            cnf.moveTimes.append(float(client.time_to_end()) - ((weight / cnf.agents[i].speed) * 1000))


if __name__ == "__main__":
    # init_game()
    main()
