'''
file in which is defined the function result comparison that plot the difference in the results between algorithm
'''

from collections import defaultdict
import random
import matplotlib.pyplot as plt
from operator import itemgetter
from typing import Set, List, Dict, Tuple
from infectionSimulation import simulate_infection

PROB_OF_BEING_INFECTED = 0.2

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

# ------------------------- forward forest -------------------------

def forward_forest (seed_set : set, filename : str, prob: float) -> List[Node]:
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

    file = (row for row in open(filename, "r"))
    filtered_edges = [(int(src), int(dst), int(unixts)) for src, dst, unixts in [line.split(split_char) for line in file] if int(dst) not in seed_set]

    for src, dst, unixts in filtered_edges:

        # check if the last_unixts is None or queal to the current unixts
        # if is equal, we'll continue to add elements to the queue
        # if is different, we'll process the queue
        if last_unixts != None and last_unixts != unixts:
            update_infection_tree (messages, infected, forest, last_unixts, prob)
        
        # if the src is infected, than the message is infected
        if src in infected:
            state = 1
        else:
            state = 0
        
        # add the tuple (src, state) to the queue
        # if the destination is already in the list, we'll add the tuple to the queue
        messages[dst].append((src, state))

        last_unixts = unixts

    update_infection_tree (messages, infected, forest, last_unixts, prob) # type: ignore
    return forest

def update_infection_tree (messages : Dict[int, List[Tuple[int, int]]], infected : Set[int], forest : List[Node], unixts : int, prob: float):
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
                    if infection_result <= prob:
                        new_node = Node(dst, unixts)
                        add_infected_edges (new_node, forest, src)
                        infected.add(dst)
                    break
            """
            previous version
            src, state = random.choice(data)
            if state == 1:
                new_node = Node(dst, unixts)
                add_infected_edges (new_node, forest, src)
                infected.add(dst) """
    messages.clear()

def add_infected_edges (new_node : Node, forest : List[Node], src: int):
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

def count_subtree_size (forest: List[Node]):
    for tree in forest:
        count_subtree_size_rec(tree)

def count_subtree_size_rec (tree: Node):
    if tree.children == []:
        tree.subtree_size = 1
    else:
        for child in tree.children:
            count_subtree_size_rec(child)
            tree.subtree_size += child.subtree_size

def choose_nodes (forest: List[Node], seed_set: Set[int], budget: int) -> Set[int]:
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

def choose_nodes_rec (tree: Node, seed_set: Set[int], max_subtree: int, node : int, set_chosen_nodes: Set[int]):
    if tree.subtree_size > max_subtree and tree.id not in seed_set and tree.id not in set_chosen_nodes:
        max_subtree = tree.subtree_size
        node = tree.id
    for child in tree.children:
        max_subtree, node = choose_nodes_rec(child, seed_set, max_subtree, node, set_chosen_nodes)
    return max_subtree, node

def find_best_node (nodes : Dict[int, int], budget : int) -> List[int]:

    # sort the nodes by their subtree size
    sorted_nodes = {k: v for k, v in sorted(nodes.items(), key=itemgetter(1), reverse=True)}
    return list(sorted_nodes.keys())[:budget]

# ------------------------- Centrality Algorithm -------------------------

def count_degree (src : int, dst : int, nodes : Dict[int, int], infected : Set[int]):
    nodes[src] += 1
    nodes[dst] += 1

# to choose the nodes with the centrality algorithm, we'll use the find_best_node function

# ------------------------- Random Algorithm -------------------------

def choose_random_nodes (budget : int, seed_set: Set[int], nodes: Set[int]):
    '''
    function that choose k nodes randomly
    input: budget is the number of nodes to choose
    output: the set of nodes chosen
    '''
    set_chosen_nodes = set()
    for _ in range(budget):
        chosen_node = random.choice(list(nodes))
        while chosen_node in seed_set or chosen_node in set_chosen_nodes:
            chosen_node = random.choice(list(nodes))
        set_chosen_nodes.add(chosen_node)
    return set_chosen_nodes

def count_nodes (src: int, dst: int, list_nodes: set[int]):
    list_nodes.add(src)
    list_nodes.add(dst)
    return list_nodes

def result_comparison(filename: str, seed_set: set, node_budget: int, subtrees: set, centrality: set, random: set, prob: float = PROB_OF_BEING_INFECTED):
    
    # dictionary that contains the number of times that each node that compare in the subtree algorithm
    removed_nodes_subtree = defaultdict(int)

    # dictionary that contains the number of times that compare in the centrality algorithm
    nodes_centrality = defaultdict(int)
    nodes = set()

    set_plot = list()

    simulate_infection (seed_set, filename, prob, set_plot, nodes=nodes_centrality, nodes_random=nodes)
    plt.plot(set_plot, label="No preventive measures", color="blue")

    """ # simulation and selection of the nodes with the subtree algorithm
    for _ in range (times):
        forest = forward_forest (seed_set, filename, prob)

        selected_node_subtree = choose_nodes (forest, seed_set, node_budget)
        for node in selected_node_subtree:
            removed_nodes_subtree[node] = removed_nodes_subtree[node] + 1

    selected_nodes_subtree = find_best_node (removed_nodes_subtree, node_budget)
    print(f"Selected nodes subtree: {selected_nodes_subtree}")
    
    for node in subtrees:
            removed_nodes_subtree[node] = removed_nodes_subtree[node] + 1"""

    set_plot = list()
    simulate_infection (seed_set, filename, prob, set_plot, subtrees)
    plt.plot(set_plot, label="subtrees", color="red")

    """ # simulation and selection of the nodes with the centrality algorithm
    selected_nodes_centrality = find_best_node (nodes_centrality, node_budget)
    print(f"Selected nodes centrality: {selected_nodes_centrality}") """

    set_plot = list()
    simulate_infection (seed_set, filename, prob, set_plot, centrality)
    plt.plot(set_plot, label="centrality measure", color="green")

    set_plot = list()
    simulate_infection (seed_set, filename, prob, set_plot, random)
    plt.plot(set_plot, label="random", color="yellow")

    plt.legend(loc="lower right", fontsize=12)
    plt.xlabel("time")
    plt.ylabel("number of infected nodes")
    #plt.show()

# ------------------------- Main -------------------------

if __name__ == "__main__":
    
    filename = "data/email.txt"

    seed_set = {83, 49, 60, 85}
    node_budget = 10
    
    subtrees_set = {43, 88, 54, 25, 66, 80, 23, 48, 16, 35}
    centrality_set = {54, 60, 71, 49, 25, 24, 48, 0, 26, 35}
    random_set = {54, 60, 71, 49, 25, 24, 48, 0, 26, 35}
    
    result_comparison(filename, seed_set, node_budget, subtrees_set, centrality_set, random_set)