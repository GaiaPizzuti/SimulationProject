'''
file that define the subtrees_methods and all the functions used in it
'''

from collections import defaultdict
import copy
import random
import igraph as ig
from matplotlib import patches
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from operator import itemgetter
from cc import Graph
import sys

from settings import *

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

# ------------------------- functions -------------------------

def infect_temporal_graph(infected : set[int], messages : dict[int, list[int]], last_unixts : int, split_char : str, file, plot : list[int], removed_nodes=[]):
    filtered_edges = [(int(src), int(dst), int(unixts)) for src, dst, unixts in [line.split(split_char) for line in file] if int(src) not in removed_nodes and int(dst) not in removed_nodes]
    for src, dst, unixts in filtered_edges:

        # check if the last_unixts is None or queal to the current unixts
        # if is equal, we'll continue to add elements to the queue
        # if is different, we'll process the queue
        if last_unixts != None and last_unixts != unixts:
            process_queue(messages, infected)
            plot.append(len(infected))

        # if the src is infected, than the message is infected
        if src in infected:
            state = 1
        else:
            state = 0

        # add the tuple (src, state) to the queue
        # if the destination is already in the list, we'll add the tuple to the queue
        messages[dst].append(state)

        last_unixts = unixts

    process_queue (messages, infected)
    plot.append(len(infected))
    return infected
    
def infect_static_graph(infected : set[int], split_char : str, file, plot : list[int], removed_nodes=[]):
    filtered_edges = [(int(src), int(dst)) for src, dst, unixts in [line.split(split_char) for line in file] if int(src) not in removed_nodes and int(dst) not in removed_nodes]

    static_graph = Graph()
    infection_tree = Forest()
    for src, dst in filtered_edges:
        static_graph.add_edge(src, dst)
                    
    previous_infected = 0
    while len(infected) != previous_infected:
        previous_infected = len(infected)
        new_infected = copy.deepcopy(infected)
        for node in infected:
            for neighbor in static_graph.adjacency_list[node]:
                if neighbor not in infected:
                    infection_result = random.uniform(0, 1)
                    if infection_result <= prob_of_being_infected:
                        new_infected.add(neighbor)
                        infection_tree.add_edge(node, neighbor)
                        # print(f"Node {neighbor} infected by {node}")
                        # print(f"Node {neighbor}'s adjacents: {infection_tree.adjacency_list[neighbor]}")
                        # print(f"Node {node}'s adjacents: {infection_tree.adjacency_list[node]}\n")
        infected = new_infected
        
    
    plot.append(len(infected))
    return infected, infection_tree

def simulate_infection(seed_set : set, filename : str, plot : list[int], removed_nodes=[]):
    '''
    simulate the infection of a graph
    input: seed_set is the set of original infected nodes, filename is the name of the file containing the graph
    output: the number of infected nodes
    '''
    
    infected = set(seed_set)

    # queue of tuples (src, state)
    messages = defaultdict(list)

    last_unixts = None
    
    split_char = ' '
    if filename == 'data/fb-forum.txt':
        split_char = ','

    file = [row for row in open(filename, "r")]
    
    if int(file[0].split(split_char)[2]) == -1:
        infected, infection_tree = infect_static_graph(infected, split_char, file, plot, removed_nodes)
    else:
        infected = infect_temporal_graph(infected, messages, last_unixts, split_char, file, plot, removed_nodes)
    
    
    return infected

def process_queue(messages : dict[int, list[int]], infected : set[int]):
    '''
    function that process the queue of messages: it choose a random message from the queue and
    if the message is infected, it will added to the infection tree
    input: messages is the queue of messages, infected is the set of infected nodes
    output: it doesn't return anything, it just update the set of infected nodes
    '''

    # for each node that has received a message, choose a random message from the queue and check if it is infected
    for dst, states in messages.items():
        infected_messages = sum(states)
        prob_of_not_being_infected = pow((1 - prob_of_being_infected), infected_messages)
        infection_result = random.uniform(0, 1)
        """ random_state = random.choice(states)
        if random_state == 1:
            infected.add(dst) """
        if infection_result > prob_of_not_being_infected:
            infected.add(dst)
    messages.clear()

# ------------------------- forward forest -------------------------

def create_forest_temporal_graph(infected : set[int], messages : dict[int, list[tuple[int, int]]], forest : list[Node], last_unixts : int, split_char : str, file) -> list[Node]:
    filtered_edges = [(int(src), int(dst), int(unixts)) for src, dst, unixts in [line.split(split_char) for line in file] if int(dst) not in infected]

    for src, dst, unixts in filtered_edges:

        # check if the last_unixts is None or queal to the current unixts
        # if is equal, we'll continue to add elements to the queue
        # if is different, we'll process the queue
        if last_unixts != None and last_unixts != unixts:
            update_infection_tree (messages, infected, forest, last_unixts)
        
        # if the src is infected, than the message is infected
        if src in infected:
            state = 1
        else:
            state = 0
        
        # add the tuple (src, state) to the queue
        # if the destination is already in the list, we'll add the tuple to the queue
        messages[dst].append((src, state))

        last_unixts = unixts

    update_infection_tree (messages, infected, forest, last_unixts) # type: ignore
    return forest

def create_forest_static_graph(infected : set[int], split_char : str, file):
    infected, infection_tree = infect_static_graph(infected, split_char, file, [])
    
    return infection_tree

def forward_forest (seed_set : set, filename : str):
    '''
    Simulation of the infection to find the forest of the infection
    input: seed_set is the set of original infected nodes, filename is the name of the file containing the graph
    output: the forest of the infection
    '''

    # final forest of the infection
    forest = list(Node(seed, -1) for seed in seed_set)
    infected = set(seed_set)

    # queue of tuples (src, state)
    messages = defaultdict(list)

    last_unixts = None
    split_char = ' '
    if filename == 'data/fb-forum.txt':
        split_char = ','

    file = [row for row in open(filename, "r")]
    if int(file[0].split(split_char)[2]) == -1:
        return create_forest_static_graph(infected, split_char, file), True
    else:
        return create_forest_temporal_graph(infected, messages, forest, last_unixts, split_char, file), False
    
    

def update_infection_tree(messages : dict[int, list[tuple[int, int]]], infected : set[int], forest : list[Node], unixts : int):
    '''
    function that process the queue of messages: it choose a random message from the queue and
    if the message is infected, it will added to the infection tree
    input: messages is the queue of messages, infected is the set of infected nodes, forest is the forest of the infection
    output: it doesn't return anything, it just update the set of infected nodes and the forest of the infection
    '''

    for dst, data in messages.items():
        if dst not in infected:
            
            for src, state in data:
                if state == 1:
                    infection_result = random.uniform(0, 1)
                    if infection_result <= prob_of_being_infected:
                        new_node = Node(dst, unixts)
                        add_infected_edges (new_node, forest, src)
                        infected.add(dst)
                    break
            """
            previously version in which we used to choose a random message and check if it was infected or not
            src, state = random.choice(data)
            if state == 1:
                new_node = Node(dst, unixts)
                add_infected_edges (new_node, forest, src)
                infected.add(dst) """
    messages.clear()

def add_infected_edges(new_node : Node, forest : list[Node], src: int):
    ''''
    function that add a new infected edge between the dst node and each src node that has the selected id
    input: new_node is the node that has been infected, forest is the forest of the infection
    output: it doesn't return anything, it just update the forest of the infection
    '''
    for tree in forest:
        if tree.id == src and tree.timestamp < new_node.timestamp:
            tree.add_child(new_node)
        else:
            add_infected_edges (new_node, tree.children, src)

# ------------------------- choose nodes -------------------------

def count_subtree_size (forest: list[Node]):
    for tree in forest:
        count_subtree_size_rec(tree)

def count_subtree_size_rec (tree: Node):
    if tree.children == []:
        tree.subtree_size = 1
    else:
        for child in tree.children:
            count_subtree_size_rec(child)
            tree.subtree_size += child.subtree_size

def choose_nodes (forest: list[Node], seed_set: set[int], budget: int) -> set[int]:
    '''
    function that choose k nodes from the forest
    input: forest is the forest of the infection, seed_set is the set of initial infected nodes, k is the number of nodes to choose
    output: the set of nodes chosen
    '''

    # count the size of the subtree of each node
    count_subtree_size(forest)


    # choose k nodes from the nodes with the highest subtree size
    set_chosen_nodes = set()
    for _ in range(budget):
        chosen_node = -1
        max_subtree = 0
        for tree in forest:
            max_subtree, chosen_node = choose_nodes_rec(tree, seed_set, max_subtree, chosen_node, set_chosen_nodes)
        set_chosen_nodes.add(chosen_node)
    
    return set_chosen_nodes

def choose_nodes_rec (tree: Node, seed_set: set[int], max_subtree: int, node : int, set_chosen_nodes: set[int]):
    if tree.subtree_size > max_subtree and tree.id not in seed_set and tree.id not in set_chosen_nodes:
        max_subtree = tree.subtree_size
        node = tree.id
    for child in tree.children:
        max_subtree, node = choose_nodes_rec(child, seed_set, max_subtree, node, set_chosen_nodes)
    return max_subtree, node

def find_best_node (nodes : dict[int, int], budget : int) -> list[int]:

    # sort the nodes by their subtree size
    sorted_nodes = {k: v for k, v in sorted(nodes.items(), key=itemgetter(1), reverse=True)}
    return list(sorted_nodes.keys())[:budget]


def sample_vrr_path(forest: Graph, seed_set: set[int]):
    '''
    function that samples a random path from the forest
    input: forest is the forest of the infection
    output: the path chosen
    '''
    # pick random node not in seed set
    filtered_forest = [node for node in forest.adjacency_list.keys() if node not in seed_set]
    if len(filtered_forest) == 0:
        return []
    
    node = random.choice(filtered_forest)
    
    # find the path from the node to the root
    path = []
    while node not in seed_set:
        # print("Retracing path from", node)
        path.append(node)
        node = list(dict.fromkeys(forest.adjacency_list[node]))[0] 
        # print(f"Node {node}'s adjacents: {forest.adjacency_list[node]}")
    return path

def subtrees_methods(filename: str, seed_set: set, node_budget: int):
    '''
    function that find the attack set of nodes that will be removed in order to minimize the spread of infections
    
    
    input:
        - filename: string, the name of the file containing the information about the network
        - seed_set: set, set of nodes selected to maximize the spread of the influence
        - node_budget: int, the maximum size of the attack set
        - prob: float, probability of a node of being infected
        
    output:
        - selected_nodes: list, attack set
    '''
    removed_nodes = defaultdict(int)

    no_prevention = list()
    
    total_length = 0
    for _ in range(times):
        first_simulation = simulate_infection (seed_set, filename, no_prevention)
        total_length += len(first_simulation)

    print(f"Infected nodes first simulation:",  total_length // times)
    
    # initialize the list of vrr paths if the graph is static
    vrr_paths = list()
    
    for _ in range (times):
        forest, is_static = forward_forest(seed_set, filename)

        if not is_static:
            selected_node = choose_nodes(forest, seed_set, node_budget)
            for node in selected_node:
                removed_nodes[node] = removed_nodes[node] + 1
        else:
            vrr_paths.append(sample_vrr_path(forest, seed_set))

    if not is_static:
        selected_nodes = find_best_node(removed_nodes, node_budget)
    else:
        # rank the nodes by the number of times they were selected and choose the top node_budget nodes
        flat_vrr_paths = [node for path in vrr_paths for node in path]
        selected_nodes = find_best_node ({node: flat_vrr_paths.count(node) for node in set(flat_vrr_paths)}, node_budget)
        
    print(f"Selected nodes: {selected_nodes}")

    prevention = list()
    
    total_infected = 0
    for _ in range(times):
        second_simulation = simulate_infection(seed_set, filename, prevention, selected_nodes)
        total_infected += len(second_simulation)
        #print(f"Infected nodes: {len(second_simulation)}")

    second_simulation = total_infected // times
    print(f"Infected nodes second infection: {second_simulation}")

    ratio = second_simulation / len(first_simulation)
    print(f"Ratio: {ratio}")
    
    return selected_nodes

# ------------------------- Main -------------------------

if __name__ == "__main__":
    
    filename = "data/email.txt"
    seed_set = {83, 49, 60, 85}
    node_budget = 10
    
    subtrees_methods(filename, seed_set, node_budget)