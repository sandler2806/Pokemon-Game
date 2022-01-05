from graph.DiGraph import DiGraph
from client_python.client import Client

gameMap: DiGraph # keeps the game map of the current level as graph

handledPokemons: list = [] # a list of all the pokemon's that was assigned an agent
edgeBank: dict[(float, float), (float, float)] = {} # contain all the edges of the graph

agents: list = [] # list of all the agents and their stats - updated 60 per seconds
pokemons: list = []  # list of all the pokemon's and their stats - updated 60 per seconds
agentsNum: int = 0

agentsPath: dict[int, [int]] = {} # keep the updated path of each agent

# critical edge, is an edge where the agent should pick up a pokemon while
# traversing it
criticalEdge: dict[int, {}] = {}

isMoved = [] # list a boolean values in the length of the agents number , keep track of agents that have moved
moveTimes = [] # keeps the
pokemonTimes = [] # pokemonTimes keeps the times we need to catch pokemon's - sorted in descending order
# final parameters
PORT = 6666 # the port of the server
HOST = '127.0.0.1' # the server ip - running on local host
is_on_way_to_pok: list = []  # tells if the agents is about to catch pokemon
dijkstra: dict[int, dict] = {} # keeps the shortest path list of all the nodes in the map
timeToEnd: float # time till the end of the game
grade: float# current grade
movecounter: int # current moves
client: Client
