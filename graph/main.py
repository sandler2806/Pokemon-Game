from graph.DiGraph import DiGraph
from graph.GraphAlgo import GraphAlgo
from client_python.config import *
from client_python.algo import *
from types import SimpleNamespace
from client_python.client import *
import json


def check():
    """
    Graph: |V|=4, |E|=5
    {0: 0: |edges_out| 1 |edges in| 1, 1: 1: |edges_out| 3 |edges in| 1, 2: 2: |edges_out| 1 |edges in| 1, 3: 3: |edges_out| 0 |edges in| 2}
    {0: 1}
    {0: 1.1, 2: 1.3, 3: 10}
    (3.4, [0, 1, 2, 3])
    (2.8, [0, 1, 3])
    (inf, [])
    (None, inf)
    2.062180280059253 [1, 10, 7]
    17.693921758901507 [47, 46, 44, 43, 42, 41, 40, 39, 15, 16, 17, 18, 19]
    11.51061380461898 [20, 21, 32, 31, 30, 29, 14, 13, 3, 2]
    inf []
    ([1, 9, 2, 3], 2.370613295323088)
    (None, inf)
    ([1, 2, 3, 4], 4.5)
    """
    # check0()
    # check1()
    # check2()
    # check3()
    my_check()


def my_check():
    PORT = 6666
    # server host (default localhost 127.0.0.1)
    HOST = '127.0.0.1'

    client = Client()
    client.start_connection(HOST, PORT)

    # pokemons = client.get_pokemons()
    # pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))
    # pokemons_obj = [p.Pokemon for p in pokemons_obj]
    pokemons = json.loads(client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]
    x, y, _ = pokemons[0].pos.split(',')
    print(type(pokemons[0]))
    graph_json = client.get_graph()

    g = DiGraph(graph_json)
    bank = g.edgeToLinear()
    print((g.edgeToLinear()))
    # y = g.nodes[9].pos[1]
    # x = g.nodes[9].pos[0]

    # x=pos[0]
    # y=pos[1]
    m = bank["9-8"][0]
    b = bank["9-8"][1]
    booli = (float(y) == m * float(x) + b)
    print(booli)
    print(abs(float(y) - (m * float(x) + b)))
    print(alocateEdge(bank, pokemons[0].pos.split(',')))
    # g = GraphAlgo()
    # file = "../data/A0.json"
    # g.load_from_json(file)
    # g.plot_graph()
    # g.graph.v_size()