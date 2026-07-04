from collections import defaultdict
from operator import itemgetter
from typing import Set, List, Dict
from infectionSimulation import simulate_infection

from settings import *

# ------------------------- choose nodes --------------------------------

def find_best_node (nodes : Dict[int, int], budget : int, seed_set: Set[int]) -> List[int]:
    # sort the nodes by their subtree size
    sorted_nodes = {k: v for k, v in sorted(nodes.items(), key=itemgetter(1), reverse=True) if k not in seed_set}
    return list(sorted_nodes.keys())[:budget]

# ------------------------- Main -------------------------

def centrality_analysis(filename: str, seed_set: set, attackset_budget: int, prob: float, nodes_centrality: Dict[int, int] = None):
    '''
    function that finds an attack set using the centrality method and simulates the infection with the attack set
    
    input:
        - filename: string, the name of the file containing the information about the network
        - seed_set: set, set of nodes selected to maximize the spread of the influence
        - attackset_budget: int, the maximum size of the attack set
        - prob: float, probability of a node of being infected
        - nodes_centrality: dict, dictionary containing the nodes and their centrality measure
        
    output:
        - total_infected_list_centrality: list, list of the number of total infected nodes for each simulation
    '''
    # simulation and selection of the nodes with the centrality algorithm
    selected_nodes_centrality = find_best_node (nodes_centrality, attackset_budget, seed_set)
    if(DEBUG): print(f"Attack set (Centrality method): {selected_nodes_centrality}")

    average_centrality = 0
    total_infected_list_centrality = []
    for _ in range(times_infection):
        second_simulation_centrality = simulate_infection (seed_set, filename, prob, removed_nodes=selected_nodes_centrality)
        average_centrality += len(second_simulation_centrality)
        total_infected_list_centrality.append(len(second_simulation_centrality))

    if(DEBUG): print(f"list of total infected nodes, centrality method: {total_infected_list_centrality}")
    
    return total_infected_list_centrality

if __name__ == "__main__":
    
    filename = "data/email.txt"
    seed_set = {83, 49, 60, 85}
    attackset_budget = 10
    subtree = set()
    
    centrality_analysis(filename, seed_set, attackset_budget, subtree)