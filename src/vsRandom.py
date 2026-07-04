import random
from typing import Set
from infectionSimulation import simulate_infection

from settings import *
from statistics import stats

# ------------------------- Random Algorithm -------------------------

def choose_random_nodes (budget : int, seed_set: Set[int], nodes: Set[int]):
    '''
    function that chooses 'budget' nodes randomly
    input: budget is the number of nodes to choose, seed_set is the set of nodes selected to maximize the spread of the influence, nodes is the set of all nodes in the graph
    output: the set of nodes chosen
    '''
    set_chosen_nodes = set()
    for _ in range(budget):
        chosen_node = rng.choice(list(nodes))
        while chosen_node in seed_set or chosen_node in set_chosen_nodes:
            chosen_node = rng.choice(list(nodes))
        set_chosen_nodes.add(chosen_node)
    return set_chosen_nodes

def random_analysis(filename: str, seed_set: set, node_budget: int, prob: float, nodes_random: Set[int] = None):
    # simulation and selection of the nodes with the random algorithm
    selected_node_random = choose_random_nodes (node_budget, seed_set, nodes_random)
    if(DEBUG): print(f"Attack set (Random method): {selected_node_random}")
    
    stats.simulation_type = "random"
    average_random = 0
    total_infected_list_random = []
    for _ in range(times_infection):
        second_simulation_random = simulate_infection (seed_set, filename, prob, removed_nodes=selected_node_random)
        average_random += len(second_simulation_random)
        total_infected_list_random.append(len(second_simulation_random))

    if(DEBUG): print(f"list of total infected nodes, random method: {total_infected_list_random}")
    
    return total_infected_list_random

# ------------------------- Main -------------------------

if __name__ == "__main__":
    
    filename = "data/email.txt"
    seed_set = {83, 49, 60, 85}
    node_budget = 20
    prob = 0.2
    random_analysis(filename, seed_set, node_budget, prob)