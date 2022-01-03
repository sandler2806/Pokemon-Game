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
    moveCounter = 0
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
    starTime = float(client.time_to_end())
    flag = 1
    while flag:
        print(client.get_agents())
        print(client.time_to_end())
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

        timePassed = starTime - float(client.time_to_end())
        if catchPokemon or False in cnf.isMoved and moveCounter <= timePassed / 100:
            cnf.moveTimes.sort(reverse=True)
            while len(cnf.moveTimes) > 0 and cnf.moveTimes[0] >= float(client.time_to_end()):
                cnf.moveTimes.pop(0)
            client.move()
            moveCounter += 1
            cnf.isMoved = [True for _ in range(cnf.agentsNum)]
            catchPokemon = False

        draw()
        assignNewPok()
        # client.move()
        clock.tick(60)

    # while True:
    #     client.move()
    #     print(client.get_agents())
    #     print(counter)
    #     print(client.get_info())
    #     counter += 1
    #     clock.tick(2)


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
            weight = cnf.gameMap.all_out_edges_of_node(cnf.agents[i].src)[Next]
            cnf.moveTimes.append(float(client.time_to_end()) - ((weight / cnf.agents[i].speed) * 1000))


if __name__ == "__main__":
    # init_game()
    main()
