from graph.DiGraph import DiGraph

gameMap: DiGraph

handledPokemons : list

agents: list
agentsNum: int

agentsPath: dict[int, [int]] = {}
# critical edges, is an edge where the agent should pick up a pokemon while
# traversing it
criticalEdge: dict[int, [tuple]] = {}
