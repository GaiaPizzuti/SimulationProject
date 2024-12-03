from copy import deepcopy
import sys
from temporalGraph import influence_maximization, spread_infection, get_random_seed_set
from subTreeInfection import subtrees_methods
from vsCentrality import centrality_analysis
from vsRandom import random_analysis
from comparison import result_comparison
from degreeNodes import degree_nodes
from cc import compare_cc
from numpy.random import Generator, PCG64, SeedSequence
from settings import *

filename = sys.argv[1]
node_budget = int(sys.argv[2])

def adversarial_attack_at_influence_maximization ():
    '''
    main function
    
    it is needed to call this function with:
        - argv[1]: the name of the relative file's path containing the graph to analyze (e.g. data/email.txt)
    '''
    
    print('---- find seed set ----\n\n')
    
    if len(sys.argv) == 4:
        seedset_budget = int(sys.argv[3])
        seed_set = get_random_seed_set(filename, seedset_budget)
    else:
        seed_set = influence_maximization(filename)
    
    print('seed set:', seed_set)
    
    print('\n\n---- simulate infection ----\n\n')
    test_seed_set = deepcopy(seed_set)
    infected = spread_infection(test_seed_set, filename)
    print('number of infected nodes in the simulation:', infected)
    
    print('\n\n---- minimize infection with subtrees ----\n\n')
    
    subtree = subtrees_methods(filename, set(seed_set), node_budget, prob_of_being_infected)
    
    print('\n\n---- minimize infection with centrality ----\n\n')
    
    centrality = centrality_analysis(filename, set(seed_set), node_budget, set(subtree), prob_of_being_infected)

    print('\n\n---- minimize infection with random ----\n\n')

    random = random_analysis(filename, set(seed_set), node_budget, prob_of_being_infected, set(subtree))
    
    print('\n\n---- result comparison ----\n\n')
    
    result_comparison(filename, set(seed_set), node_budget, set(subtree), set(centrality), set(random), prob_of_being_infected)
    
    degree_nodes(filename, subtree, centrality)
    
    compare_cc(filename, subtree, centrality)
    
    return subtree

if __name__ == '__main__':
    """
    Args:
        - filename: the name of the relative file's path containing the graph to analyze
        - node_budget: the number of nodes to select
    
    settings.py:
            - prob_of_being_infected: the probability of being infected
            - method: the method to use for the simulation
            - times: the number of times to loop the simulation

    """
    
    total_selected_nodes = []
    for i in range(times_main):
        rng = generators[i]
        selected_nodes = adversarial_attack_at_influence_maximization()
        total_selected_nodes.append(selected_nodes)
    
    print('total selected nodes:')
    for selected_nodes in total_selected_nodes:
        print(selected_nodes)