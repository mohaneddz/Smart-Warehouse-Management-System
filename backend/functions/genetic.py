# >>> IMPORTANT NOTE <<< 
# THIS IS AN EXAMPLE OF THE ALGORITHM IMPLEMENTATION.
# IT IS JUST AN EXAMPLE FOR HOW TO USE THE OTHER FILES IN THE BACKEND.

from typing import List
from core.warehouse import Node
import random

def genetic_algorithm(start: Node, goal: Node, population_size: int = 100, generations: int = 100) -> List[Node]:
    """Wrapper function for the Genetic Algorithm.
    
    Args:
        start: The starting node
        goal: The goal node
        population_size: Size of the population for each generation
        generations: Number of generations to evolve
        
    Returns:
        List[Node]: The best path found
    """
    search = GeneticAlgorithm(start, goal, population_size, generations)
    return search.search()

class GeneticAlgorithm:
    def __init__(self, start: Node, goal: Node, population_size: int = 100, generations: int = 100):
        self.start = start
        self.goal = goal
        self.population_size = population_size
        self.generations = generations
        self.population = []

    def search(self) -> List[Node]:
        """ Perform Genetic Algorithm to find the optimal path. """
        self._initialize_population()
        for generation in range(self.generations):
            self._evolve_population()
            best_solution = self._get_best_solution()
            if best_solution == self.goal:
                return best_solution
        return self._get_best_solution()

    def _initialize_population(self):
        """ Generate the initial population. """
        self.population = [self._random_solution() for _ in range(self.population_size)]

    def _random_solution(self) -> List[Node]:
        """ Generate a random solution (path). """
        return [self.start, self.goal]

    def _evolve_population(self):
        """ Evolve the population by selecting the best solutions and applying crossover and mutation. """
        new_population = []
        for i in range(self.population_size):
            parent1, parent2 = self._select_parents()
            child = self._crossover(parent1, parent2)
            self._mutate(child)
            new_population.append(child)
        self.population = new_population

    def _select_parents(self) -> tuple:
        """ Select two parents from the population. """
        return random.choice(self.population), random.choice(self.population)

    def _crossover(self, parent1: List[Node], parent2: List[Node]) -> List[Node]:
        """ Perform crossover between two parent solutions. """
        return parent1[:len(parent1) // 2] + parent2[len(parent2) // 2:]

    def _mutate(self, solution: List[Node]):
        """ Perform mutation on a solution. """
        mutation_point = random.randint(0, len(solution) - 1)
        solution[mutation_point] = self.start

    def _get_best_solution(self) -> List[Node]:
        """ Get the best solution in the population. """
        return min(self.population, key=self._fitness)

    def _fitness(self, solution: List[Node]) -> float:
        """ Calculate the fitness of a solution (path). """
        return sum(self.get_distance(solution[i], solution[i+1]) for i in range(len(solution) - 1))

    def get_distance(self, n1: Node, n2: Node) -> float:
        """ Calculate Euclidean distance between two nodes. """
        return (n1.x - n2.x) ** 2 + (n1.y - n2.y) ** 2
