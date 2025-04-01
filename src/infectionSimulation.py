import random
from collections import defaultdict
from typing import Set, List, Dict
from cc import Graph, Forest
from copy import deepcopy

from settings import *
from statistics import *

def infect_temporal_graph(infected : "set[int]", messages : "dict[int, list[int]]", last_unixts : int, split_char : str, file, prob: float, plot=[], removed_nodes=[], nodes=defaultdict(int), nodes_random=set()):
    '''
    Function to simulate the spread of an infection in a temporal graph
    input:
        - infected: the set of original infected nodes
        - messages: the queue of messages
        - last_unixts: the last unixts
        - split_char: the character that split the lines of the file
        - file: the file containing the graph
        - prob: the probability of being infected
        - removed_nodes: the set of nodes that have been removed
    output:
        - the set of infected nodes
    '''

    stats.current_infected_nodes = []
    filtered_edges = [(int(src), int(dst), int(unixts)) for src, dst, unixts in [line.split(split_char) for line in file] if int(src) not in removed_nodes and int(dst) not in removed_nodes]
    for src, dst, unixts in filtered_edges:

        if removed_nodes == []:
            count_degree(src, dst, nodes, infected)
            count_nodes(src, dst, nodes_random)

        # check if the last_unixts is None or queal to the current unixts
        # if is equal, we'll continue to add elements to the queue
        # if is different, we'll process the queue
        if last_unixts != None and last_unixts != unixts:
            process_queue (messages, infected, prob)
            plot.append(len(infected))
            stats.current_infected_nodes.append(len(infected))

        # if the src is infected, than the message is infected
        if src in infected:
            state = 1
        else:
            state = 0

        # add the tuple (src, state) to the queue
        # if the destination is already in the list, we'll add the tuple to the queue
        messages[dst].append(state)

        last_unixts = unixts

    process_queue (messages, infected, prob)
    plot.append(len(infected))
    stats.current_infected_nodes.append(len(infected))
    stats.save_infected_nodes_list()
    return infected
    
def infect_static_graph(infected : "set[int]", split_char : str, file, prob: float, plot=[], removed_nodes=[], nodes=defaultdict(int), nodes_random=set()):
    '''
    Function to simulate the spread of an infection in a static graph
    input:
        - infected: the set of original infected nodes
        - split_char: the character that split the lines of the file
        - file: the file containing the graph
        - prob: the probability of being infected
        - removed_nodes: the set of nodes that have been removed
    output:
        - the set of infected nodes
    '''
    
    filtered_edges = [(int(src), int(dst)) for src, dst, unixts in [line.split(split_char) for line in file] if int(src) not in removed_nodes and int(dst) not in removed_nodes]

    static_graph = Graph()
    infection_tree = Forest()
    for src, dst in filtered_edges:
        static_graph.add_edge(src, dst)
        if removed_nodes == []:
            count_degree(src, dst, nodes, infected)
            count_nodes(src, dst, nodes_random)
                    
    previous_infected = 0
    plot.append(len(infected))
    stats.current_infected_nodes = []
    stats.current_infected_nodes.append(len(infected))
    while len(infected) != previous_infected:
        previous_infected = len(infected)
        new_infected = deepcopy(infected)
        for node in infected:
            for neighbor in static_graph.adjacency_list[node]:
                if neighbor not in infected:
                    infection_result = rng.uniform(0, 1)
                    if infection_result <= prob:
                        new_infected.add(neighbor)
                        infection_tree.add_edge(node, neighbor)
                        # print(f"Node {neighbor} infected by {node}")
                        # print(f"Node {neighbor}'s adjacents: {infection_tree.adjacency_list[neighbor]}")
                        # print(f"Node {node}'s adjacents: {infection_tree.adjacency_list[node]}\n")
        infected = new_infected
        plot.append(len(infected))
        stats.current_infected_nodes.append(len(infected))
        
    stats.save_infected_nodes_list()
    return infected, infection_tree

def simulate_infection(seed_set : set, filename : str, prob: float, plot=[], removed_nodes=[], nodes=defaultdict(int), nodes_random=set()):
    '''
    Function to simulate the spread of an infection in a temporal graph
    input:
        - seed_set: the set of original infected nodes
        - filename: the name of the file containing the graph
        - plot: the list of the number of infected nodes at each time step
        - prob: the probability of being infected
        - removed_nodes: the set of nodes that have been removed
    output:
        - the number of infected nodes
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
        infected, infection_tree = infect_static_graph(infected, split_char, file, prob, plot, removed_nodes, nodes, nodes_random)
    else:
        infected = infect_temporal_graph(infected, messages, last_unixts, split_char, file, prob, plot, removed_nodes, nodes, nodes_random)
    
    
    return infected

def process_queue (messages : Dict[int, List[int]], infected : Set[int], prob: float):
    '''
    function that process the queue of messages: it choose a random message from the queue and
    if the message is infected, it will added to the infection tree
    input: messages is the queue of messages, infected is the set of infected nodes
    output: it doesn't return anything, it just update the set of infected nodes
    '''

    # for each node that has received a message, choose a random message from the queue and check if it is infected
    for dst, states in messages.items():
        """
        previous version
        random_state = rng.choice(states)
        if random_state == 1:
            infected.add(dst) """
        infected_messages = sum(states)
        prob_of_not_being_infected = pow((1 - prob), infected_messages)
        infection_result = rng.uniform(0, 1)
        if infection_result > prob_of_not_being_infected:
            infected.add(dst)
    messages.clear()



# ------------------------- Centrality Algorithm -------------------------

def count_degree (src : int, dst : int, nodes : Dict[int, int], infected : Set[int]):
    nodes[src] += 1
    nodes[dst] += 1

# ------------------------- Random Algorithm -------------------------

def count_nodes (src: int, dst: int, list_nodes: set[int]):
    list_nodes.add(src)
    list_nodes.add(dst)
    return list_nodes