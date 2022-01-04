from graph.DiGraph import DiGraph

gameMap: DiGraph

handledPokemons: list = []
edgeBank: dict[(float, float), (float, float)] = {}

agents: list = []
pokemons: list = []
agentsNum: int = 0

agentsPath: dict[int, [int]] = {}
# critical edges, is an edge where the agent should pick up a pokemon while
# traversing it
criticalEdge: dict[int, []] = {}
isMoved = []
moveTimes=[]
pokemonTimes=[]
# final parameters
PORT = 6666
HOST = '127.0.0.1'
# HOST='10.9.7.71'
is_on_way_to_pok: list = []  # initiated in "dispatchAgents" (in algo.c)
dijkstra: dict[int,dict]={}
timeToEnd:float
