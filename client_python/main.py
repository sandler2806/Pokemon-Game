import json
from types import SimpleNamespace
from GUI import *
from client_python.client import Client
from graph.DiGraph import DiGraph
from client_python.algo import allocateAgent , dispatchAgents
import client_python.config as cnf

client: Client


def main():

    global client
    client = Client()
    client.start_connection(cnf.HOST, cnf.PORT)

    print(client.get_agents())
    # dispach as much agents as possible
    dispatchAgents(client)
    # load the map to graph
    cnf.gameMap = DiGraph(client.get_graph())
    # assigning the starting Pokemon's
    assignNewPok()

    init_GUI()
    # start the game
    client.start()
    flag = 1
    while flag:
        # assigning an agent for new pokemon's from the server
        assignNewPok()
        # check if any of the agents need to 'Move'
        cnf.agents = json.loads(client.get_agents(),
                            object_hook=lambda d: SimpleNamespace(**d)).Agents

        # print(agentsStatus)
        for i in range(cnf.agentsNum):
            if len(cnf.is_on_way_to_pok[i]) != 0:
                for pos in cnf.is_on_way_to_pok[i]:
                    pass

        flag = 0

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
    pokemons = json.loads(client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]

    # look for new Pokemon's
    for pok in pokemons:
        if not isHandled(pok):
            allocateAgent(pok)
            cnf.handledPokemons.append(pok)

def set_next_node(id : int):

    for i in range(cnf.agentsNum):
        if cnf.agents[i]['Agent']['dest'] == -1 and len(cnf.agentsPath[i]):



if __name__ == "__main__":
    # init_game()
    main()