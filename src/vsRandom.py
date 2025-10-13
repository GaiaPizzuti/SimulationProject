# ------------------------- class Node -------------------------

import random
from typing import Set
from infectionSimulation import simulate_infection
from subTreeInfection import subtrees_methods
from numpy.random import Generator, PCG64, SeedSequence

from settings import *
from statistics import stats # type: ignore

PROB_OF_BEING_INFECTED = 0.2

class Node:
    
    def __init__(self, id, timestamp):
        ''''
        init function of the class Node
        '''
        self.id = id
        self.timestamp = timestamp
        self.children = []
        self.subtree_size = 0

    def add_child(self, child):
        '''
        add a child to the node
        '''
        self.children.append(child)

    def __repr__(self):
        return f"{self.id}, {self.timestamp}"
    
# ------------------------ print tree ------------------------

def print_tree(tree, spaces=0):
    ''''
    function that print the tree as an horizontal tree
    if spaces are passed in input, the tree will be printed with the number of spaces passed in input
    '''
    print(" " * spaces, tree)
    for child in tree.children:
        print_tree(child, spaces+1)


# ------------------------- Random Algorithm -------------------------

def choose_random_nodes (budget : int, seed_set: Set[int], nodes: Set[int]):
    '''
    function that choose k nodes randomly
    input: budget is the number of nodes to choose
    output: the set of nodes chosen
    '''
    set_chosen_nodes = set()
    for _ in range(budget):
        chosen_node = rng.choice(list(nodes))
        while chosen_node in seed_set or chosen_node in set_chosen_nodes:
            chosen_node = rng.choice(list(nodes))
        set_chosen_nodes.add(chosen_node)
    return set_chosen_nodes

def random_analysis(filename: str, seed_set: set, node_budget: int, prob: float = PROB_OF_BEING_INFECTED, selected_nodes_subtree = []):

    # set that contains all the nodes of the graph
    nodes = set()


    first_simulation = simulate_infection (seed_set, filename, prob, nodes_random=nodes)
    # print(f"First simulation: {len(first_simulation)}")

    if selected_nodes_subtree == []:
        selected_nodes_subtree = subtrees_methods(filename, set(seed_set), node_budget, prob)
   
    # print(f"Selected nodes (Subtree method): {selected_nodes_subtree}")

    average_subtree = 0
    for _ in range(times):
        second_simulation_subtree = simulate_infection (seed_set, filename, prob, removed_nodes=selected_nodes_subtree)
        average_subtree += len(second_simulation_subtree)
    # print(f"Average number of infected nodes, subtree method: {average_subtree/times}")

    # simulation and selection of the nodes with the random algorithm
    selected_node_random = choose_random_nodes (node_budget, seed_set, nodes)
    # print(f"Selected nodes (Random method): {selected_node_random}")
    
    stats.simulation_type = "random"
    average_random = 0
    for _ in range(times):
        second_simulation_random = simulate_infection (seed_set, filename, prob, removed_nodes=selected_node_random)
        average_random += len(second_simulation_random)
    # print(f"Average number of infected nodes, random method: {average_random/times}")
    stats.simulation_type = "none"

    mean_infected = average_random / times
    
    return selected_node_random, mean_infected

# ------------------------- Main -------------------------

if __name__ == "__main__":
    
    filename = "data/email.txt"
    seed_set = {83, 49, 60, 85}
    node_budget = 20
    random_analysis(filename, seed_set, node_budget)