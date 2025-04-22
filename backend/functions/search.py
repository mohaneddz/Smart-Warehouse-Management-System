# >>> IMPORTANT NOTE <<< 
# THIS IS AN EXAMPLE OF THE ALGORITHM IMPLEMENTATION.
# IT IS JUST AN EXAMPLE FOR HOW TO USE THE OTHER FILES IN THE BACKEND.

from core.warehouse import Node
from backend.functions.a_star import AStarSearch
from backend.functions.greedy import GreedySearch
from backend.functions.simulated_annealing import SimulatedAnnealing
from backend.functions.genetic import GeneticAlgorithm

def search(algorithm: str, start: Node, goal: Node):
    """ Run the selected search algorithm and return the result. """
    if algorithm == "AStar":
        search = AStarSearch(start, goal)
        return search.search()
    elif algorithm == "Greedy":
        search = GreedySearch(start, goal)
        return search.search()
    elif algorithm == "SimulatedAnnealing":
        search = SimulatedAnnealing(start, goal)
        return search.search()
    elif algorithm == "Genetic":
        search = GeneticAlgorithm(start, goal)
        return search.search()
    else:
        raise ValueError(f"Unknown algorithm {algorithm}")
