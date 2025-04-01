# ------------------------- class Node -------------------------

from collections import defaultdict
from operator import itemgetter
from typing import Set, List, Dict
from infectionSimulation import simulate_infection
from numpy.random import Generator, PCG64, SeedSequence

from settings import *
from statistics import *

PROB_OF_BEING_INFECTED = 0.8

# ------------------------- class Tree -------------------------

class Forest:
    # constructor
    def __init__(self):
        # initialize adjacency list
        self.adjacency_list = defaultdict(dict)
        
    def add_edge(self, src, dst):
        if src not in self.adjacency_list:
            self.adjacency_list[src] = dict()
        if dst not in self.adjacency_list:
            self.adjacency_list[dst] = dict()
            
        self.adjacency_list[src][dst] = None
        self.adjacency_list[dst][src] = None
    
    def add_node(self, node):
        if node not in self.adjacency_list:
            self.adjacency_list[node] = dict()
    
    def get_adjacency_list(self):
        return {k: list(v.keys()) for k, v in self.adjacency_list.items()}


# ------------------------- class Node -------------------------

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

# ------------------------- choose nodes --------------------------------

def find_best_node (nodes : Dict[int, int], budget : int, seed_set: Set[int]) -> List[int]:

    # sort the nodes by their subtree size
    sorted_nodes = {k: v for k, v in sorted(nodes.items(), key=itemgetter(1), reverse=True) if k not in seed_set}
    return list(sorted_nodes.keys())[:budget]

# to choose the nodes with the centrality algorithm, we'll use the find_best_node function

# ------------------------- Main -------------------------

def centrality_analysis(filename: str, seed_set: set, node_budget: int, selected_nodes_subtree: set, prob: float = PROB_OF_BEING_INFECTED):

    # dictionary that contains the number of times that each node that compare in the subtree algorithm
    #removed_nodes_subtree = defaultdict(int)

    # dictionary that contains the number of times that compare in the centrality algorithm
    nodes_centrality = defaultdict(int)


    simulate_infection (seed_set, filename, prob, nodes=nodes_centrality)

    """ # simulation and selection of the nodes with the subtree algorithm
    for _ in range (times):
        forest = forward_forest (seed_set, filename, prob)

        selected_node_subtree = choose_nodes (forest, seed_set, node_budget)
        for node in selected_node_subtree:
            removed_nodes_subtree[node] = removed_nodes_subtree[node] + 1

    selected_nodes_subtree = find_best_node (removed_nodes_subtree, node_budget)
    print(f"Selected nodes subtree: {selected_nodes_subtree}") """

    print(f"Selected nodes (Subtree method): {selected_nodes_subtree}")

    average_subtree = 0
    for _ in range(times):
        second_simulation_subtree = simulate_infection (seed_set, filename, prob, removed_nodes=selected_nodes_subtree)
        average_subtree += len(second_simulation_subtree)
    print(f"Average number of infected nodes, subtree method: {average_subtree/times}")

    # simulation and selection of the nodes with the centrality algorithm
    selected_nodes_centrality = find_best_node (nodes_centrality, node_budget, seed_set)
    print(f"Selected nodes (Centrality method): {selected_nodes_centrality}")

    stats.simulation_type = "centrality"
    average_centrality = 0
    for _ in range(times):
        second_simulation_centrality = simulate_infection (seed_set, filename, prob, removed_nodes=selected_nodes_centrality)
        average_centrality += len(second_simulation_centrality)
    print(f"Average number of infected nodes, centrality method: {average_centrality/times}")
    stats.simulation_type = "none"

    ratio = average_subtree/average_centrality
    print(f"Ratio between the two methods (lower = subtree method is better): {ratio}")
    
    return selected_nodes_centrality

if __name__ == "__main__":
    
    filename = "data/email.txt"
    seed_set = {83, 49, 60, 85}
    node_budget = 10
    subtree = set()
    
    centrality_analysis(filename, seed_set, node_budget, subtree)