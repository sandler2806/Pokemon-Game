from graph.DiGraph import DiGraph
from graph.GraphAlgo import GraphAlgo
from client_python.client import *
import json


def alocateEdge(bank: dict[str, (float, float)], pos: list):
    x = pos[0]
    y = pos[1]

    for edge, mb in bank.items():
        m = mb[0]
        b = mb[1]
        booli = (float(y) == m * float(x) + b)
        if booli:
            return edge
    return None
