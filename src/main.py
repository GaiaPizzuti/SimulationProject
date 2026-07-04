from copy import deepcopy
import sys
import numpy as np

from temporalGraph import influence_maximization, get_random_seed_set
from subTreeInfection import subtrees_methods, simulate_infection
from vsCentrality import centrality_analysis
from vsRandom import random_analysis
from infectionSimulation import simulate_infection, FILE_ALREADY_OPENED
from numpy.random import Generator, PCG64, SeedSequence
from settings import DEBUG, prob_of_being_infected, times_main, times_infection, generators, rng, entropy
from statistics import stats
import matplotlib.pyplot as plt
import time
from collections import defaultdict

def validate_input_parameters():
    '''
    function to validate the input parameters from the command line arguments
    
    output:
        - filename: the name of the relative file's path containing the graph to analyze
        - attackset_budget: the number of nodes to select for the adversarial attack
        - seedset_budget: the number of nodes to select for the seed set (if None, the seed set will be selected using the influence maximization algorithm)
    '''
    if(DEBUG): print('\n---- validating input parameters ----')
    if len(sys.argv) == 3:
        filename = sys.argv[1]
        attackset_budget = int(sys.argv[2])
        seedset_budget = None
    elif len(sys.argv) == 4:
        filename = sys.argv[1]
        attackset_budget = int(sys.argv[2])
        seedset_budget = int(sys.argv[3])
    elif len(sys.argv) == 6:
        filename = sys.argv[1]
        attackset_budget = int(sys.argv[2])
        seedset_budget = None
    else:
        print("Usage: python main.py <filename> <attackset_budget> [<seedset_budget> | <times_main> <times_infection> <prob_of_being_infected>]")
        sys.exit(1)
    return filename, attackset_budget, seedset_budget

def get_seed_set(filename, seedset_budget):
    '''
    function to get the seed set from the influence maximization algorithm or from a random selection of nodes if the seedset_budget is not None

    output:
        - seed_set: the set of nodes to use as seed set for the infection simulation
    '''
    if(DEBUG): print('\n---- getting seed set ----')
    if seedset_budget is not None and seedset_budget > 0:
        seed_set = get_random_seed_set(filename, seedset_budget)
    else:
        seed_set = influence_maximization(filename)
    if(DEBUG): print('Chosen seed set:', seed_set)

    return seed_set

def adversarial_attack_at_influence_maximization(attackset_budget, seed_set):
    '''
    function to perform adversarial attack

    input:
        - attackset_budget: the number of nodes to select for the adversarial attack
        - seed_set: the set of nodes to use as seed set for the infection simulation
    output:
        - attack_sets: a list of the three different attack sets (subtree, centrality, random)
        - means: a list of the three different means of infected nodes (subtree, centrality, random)
        - len(infected): the number of infected nodes in the simulation without any adversarial attack
    '''
    
    # simulate the infection without attack set, then with the three different methods to get the number of infected nodes
    if(DEBUG): print('\n---- simulating infection without attack set ----')
    naive_total_infected_nodes = list()
    # when we simulate the first infection without attack set, save information needed for the centrality and random methods 
    nodes_centrality = defaultdict(int)
    nodes_random = set()
    for _ in range(times_infection):
        first_simulation = simulate_infection(seed_set, filename, prob_of_being_infected, removed_nodes=[], nodes_centrality=nodes_centrality, nodes_random=nodes_random)
        naive_total_infected_nodes.append(len(first_simulation))
    if(DEBUG): print(f"list of total infected nodes, no attack set employed: {naive_total_infected_nodes}")

    if(DEBUG): print('\n---- minimizing infection with Baseline Method ----')
    subtrees_total_infected_nodes = subtrees_methods(filename, set(seed_set), attackset_budget, prob_of_being_infected)
    
    if(DEBUG): print('\n---- minimizing infection with Centrality Method ----')
    centrality_total_infected_nodes = centrality_analysis(filename, set(seed_set), attackset_budget, prob_of_being_infected, nodes_centrality=nodes_centrality)

    if(DEBUG): print('\n---- minimizing infection with Random Method ----')
    random_total_infected_nodes = random_analysis(filename, set(seed_set), attackset_budget, prob_of_being_infected, nodes_random=nodes_random)

    stats.naive_total_infected_nodes.append(naive_total_infected_nodes)
    stats.subtrees_total_infected_nodes.append(subtrees_total_infected_nodes)
    stats.centrality_total_infected_nodes.append(centrality_total_infected_nodes)
    stats.random_total_infected_nodes.append(random_total_infected_nodes)

def plot_average_infection(average_infection, time):
    '''
    function to plot the average of the node speed as a function of time
    '''
    label = 'Average infected nodes'
    plt.plot(time, average_infection, label=label)
    plt.xlabel('Epoch')
    plt.ylabel('Average infected nodes')
    plt.title('Average number of nodes infected as a function of time epochs')
    plt.grid()

def plot_results(time, mean, lower_bound, upper_bound, mean_overall):
    '''
    function to plot the mean, the variance, the lower bound and the upper bound of the average number of infected nodes by time
    '''
    plt.plot(time, mean, label='Mean infected nodes', color='b')
    plt.hlines(mean_overall, xmin=time[0], xmax=time[-1], colors='r', linestyles='dashed', label='Mean overall')
    plt.fill_between(time, lower_bound, upper_bound, color='b', alpha=0.2, label='Confidence Interval')
    plt.xlabel('Epoch')
    plt.ylabel('Number of infected nodes')
    plt.title('Number of infected nodes as a function of time epochs')
    plt.legend()
    plt.grid()
    plt.show()

def plot_infections():
    '''
    function to plot the number of infected nodes by time
    '''
    plt.plot(stats.naive_infected_nodes_by_time, label='Naive')
    plt.plot(stats.subtrees_infected_nodes_by_time, label='Subtrees')
    plt.plot(stats.centrality_infected_nodes_by_time, label='Centrality')
    plt.plot(stats.random_infected_nodes_by_time, label='Random')
    plt.xlabel('Epoch')
    plt.ylabel('Number of infected nodes')
    plt.title('Number of infected nodes as a function of time epochs')
    plt.legend()
    plt.grid()
    plt.show()

def plot_ratio(centrality, random, centrality_random):
    '''
    function to plot the ratio between the number of infected nodes of the subtree method and the other methods
    '''
    plt.plot(centrality, label='Subtree / Centrality')
    plt.plot(random, label='Subtree / Random')
    plt.plot(centrality_random, label='Centrality / Random')
    plt.xlabel('Indipendent Replications')
    plt.ylabel('Ratio of infected nodes')
    plt.title('Ratio of infected nodes during different simulations')
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == '__main__':
    """
    main function. handles input, executes AAIM and handles output 
    """

    filename, attackset_budget, seedset_budget = validate_input_parameters()

    seed_set = get_seed_set(filename, seedset_budget)

    first_infections = list()

    for i in range(times_main):
        if(DEBUG): print(f'\n---- starting Repetition {i+1}/{times_main} ----')
        rng = generators[i]
        adversarial_attack_at_influence_maximization(attackset_budget, seed_set)


    stats.output_analysis()

    print(f'\n--------------- Influence Spread statistics with the different methods ---------------')
    print('subtrees mean, variance, lower bound and upper bound:')
    print(stats.subtrees_grand_mean, stats.subtrees_variance, stats.subtrees_lower_bound[0], stats.subtrees_upper_bound[0])

    print('centrality mean, variance, lower bound and upper bound:')
    print(stats.centrality_grand_mean, stats.centrality_variance, stats.centrality_lower_bound[0], stats.centrality_upper_bound[0])

    print('random mean, variance, lower bound and upper bound:')
    print(stats.random_grand_mean, stats.random_variance, stats.random_lower_bound[0], stats.random_upper_bound[0])

    #plot_infections()

    print(f'\n---- Improvement in graph resistance with the different methods (lower is better) ----')
    print(f"Subtree improvement: {np.mean(stats.improvement_subtree)}")
    print(f"Centrality improvement: {np.mean(stats.improvement_centrality)}")
    print(f"Random improvement: {np.mean(stats.improvement_random)}")

    # save the image in the output folder
    filename = filename.split('/')[-1].split('.')[0]
    prob = str(prob_of_being_infected).replace('.', '_')
    plt.savefig(f'output3/ratio_{filename}_{times_infection}_{times_main}_{prob}.png')

