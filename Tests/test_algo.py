import json
from types import SimpleNamespace
from unittest import TestCase
import client_python.config as cnf
from graph.DiGraph import DiGraph
from client_python.algo import Algo


class Test(TestCase):
    cnf.pokemons = json.loads("""
       {
            "Pokemons":[
                {
                    "Pokemon":{
                        "value":5.0,
                        "type":-1,
                        "pos":"35.25656770719604,32.3091878639921,0.0"
                    }
                },{
                    "Pokemon":{
                        "value":8.0,
                        "type":-1,
                        "pos":"35.87656770719604,32.8191878639921,0.0"
                    }
                },{
                    "Pokemon":{
                        "value":10.0,
                        "type":1,
                        "pos":"35.97656770719604,32.0191878639921,0.0"
                    }
                }
            ]
        }
       
        """,
                              object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    cnf.pokemons = [p.Pokemon for p in cnf.pokemons]

    cnf.agents = json.loads("""
     {
            "Agents":[
                {
                    "Agent":
                    {
                        "id":0,
                        "value":0.0,
                        "src":0,
                        "dest":1,
                        "speed":1.0,
                        "pos":"35.18753053591606,32.10378225882353,0.0"
                    }
                }
            ]
        }
     """,
                            object_hook=lambda d: SimpleNamespace(**d)).Agents

    cnf.agents = [agent.Agent for agent in cnf.agents]
    cnf.agentsPath[0] = []
    f = open("../data/A0")
    graphJ = json.load(f)
    strG = json.dumps(graphJ)
    graph = DiGraph(strG)
    cnf.gameMap = graph
    cnf.edgeBank = cnf.gameMap.edgeToLinear()
    for node in cnf.gameMap.nodes.values():
        cnf.dijkstra[node.id] = Algo.dijkstra(node.id)[1]
    cnf.criticalEdge[0] = []

    def test_allocate_agent(self):

        Algo.allocateAgent(cnf.pokemons[1])
        self.assertEqual(cnf.criticalEdge,{0: [(1, 0)]})
        self.assertEqual((cnf.agentsPath,{0: [0]}))
        print(cnf.criticalEdge)
        print(cnf.agentsPath)

        Algo.allocateAgent(cnf.pokemons[2])
        self.assertEqual(cnf.criticalEdge,{0: [(1, 0), (0, 10)]})
        self.assertEqual((cnf.agentsPath,{0: [0, 10]}))
        print(cnf.criticalEdge)
        print(cnf.agentsPath)
        Algo.allocateAgent(cnf.pokemons[0])
        self.assertEqual(cnf.criticalEdge,{0: [(1, 0)]})
        self.assertEqual((cnf.agentsPath,{0: [0]}))
        print(cnf.criticalEdge)
        print(cnf.agentsPath)

    def test_allocateEdge(self):
        x, y, _ = cnf.pokemons[0].pos.split(',')
        newEdge = Algo.allocateEdge(cnf.edgeBank, [x, y], cnf.pokemons[0].type)
        self.assertEqual(newEdge, (7, 6))

        x, y, _ = cnf.pokemons[1].pos.split(',')
        newEdge = Algo.allocateEdge(cnf.edgeBank, [x, y], cnf.pokemons[1].type)
        self.assertEqual(newEdge, (1, 0))

        x, y, _ = cnf.pokemons[2].pos.split(',')
        newEdge = Algo.allocateEdge(cnf.edgeBank, [x, y], cnf.pokemons[2].type)
        self.assertEqual(newEdge, (0, 10))
