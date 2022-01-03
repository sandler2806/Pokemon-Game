import json
from types import SimpleNamespace
from GUI import *
import pygame
from client_python.client import Client
from graph.DiGraph import DiGraph
from client_python.algo import allocateAgent, dispatchAgents
import client_python.config as cnf

client: Client


def main():
    global client
    counter = 0
    clock = pygame.time.Clock()
    EPS = 0.001
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
    flag = 1
    while flag:
        # print(client.get_agents())
        print(counter)
        counter += 1
        # assigning an agent for new pokemon's from the server
        # check if any of the agents need to 'Move'

        set_next_node()
        # print(agentsStatus)
        for agent in cnf.agents:
            if len(cnf.is_on_way_to_pok[agent.id]) != 0:
                for pos in cnf.is_on_way_to_pok[agent.id]:
                    x, y, _ = agent.pos.split(',')
                    if abs(pos[0] - x) < EPS and abs(pos[1] - y) < EPS:
                        catchPokemon = True
                        cnf.is_on_way_to_pok[agent.id].remove(pos)

        if catchPokemon or False in cnf.isMoved:
            client.move()
            cnf.isMoved = [True for _ in range(cnf.agentsNum)]
            catchPokemon = False

        # draw()
        assignNewPok()
        clock.tick(2)


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
    for i in range(cnf.agentsNum):
        if cnf.agents[i].dest == -1 and len(cnf.agentsPath[i]) and cnf.isMoved[i]:
            cnf.isMoved[i] = False
            Next = cnf.agentsPath[i].pop(0)
            client.choose_next_edge('{"agent_id":' + str(i) + ', "next_node_id":' + str(Next) + '}')


if __name__ == "__main__":
    # init_game()
    main()
