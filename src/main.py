from copy import deepcopy
import sys
import numpy as np

from temporalGraph import influence_maximization, spread_infection, get_random_seed_set
from subTreeInfection import subtrees_methods
from vsCentrality import centrality_analysis
from vsRandom import random_analysis
from numpy.random import Generator, PCG64, SeedSequence
from settings import *
from statistics import stats # type: ignore
import matplotlib.pyplot as plt

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
    
    #stats.simulation_type = "subtrees"
    subtree = subtrees_methods(filename, set(seed_set), node_budget, prob_of_being_infected)
    
    print('\n\n---- minimize infection with centrality ----\n\n')
    
    #stats.simulation_type = "centrality"
    centrality = centrality_analysis(filename, set(seed_set), node_budget, set(subtree), prob_of_being_infected)

    print('\n\n---- minimize infection with random ----\n\n')

    #stats.simulation_type = "random"
    random = random_analysis(filename, set(seed_set), node_budget, prob_of_being_infected, set(subtree))
    
    print('\n\n---- result comparison ----\n\n')
    
    #result_comparison(filename, set(seed_set), node_budget, set(subtree), set(centrality), set(random), prob_of_being_infected)
    
    #degree_nodes(filename, subtree, centrality)
    
    #compare_cc(filename, subtree, centrality)
    
    return subtree, centrality, random

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

def plot_results(time, mean, lower_bound, upper_bound):
    '''
    function to plot the mean, the variance, the lower bound and the upper bound of the average number of infected nodes by time
    '''
    plt.plot(time, mean, label='Mean')
    plt.fill_between(time, lower_bound, upper_bound, alpha=0.2, label='95% Confidence interval')
    plt.legend(loc='upper right')
    #plt.ylim(0, V_MAX)
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
        stats.subtrees_attack_set.append(selected_nodes[0])
        stats.centrality_attack_set.append(selected_nodes[1])
        stats.random_attack_set.append(selected_nodes[2])

    
    print('total selected nodes:')
    for selected_nodes in total_selected_nodes:
        print(selected_nodes)

    print('subtrees infected nodes by time:')
    print(stats.subtrees_infected_nodes_by_time)

    print('centrality infected nodes by time:')
    print(stats.centrality_infected_nodes_by_time)
    
    print('random infected nodes by time:')
    print(stats.random_infected_nodes_by_time)

    stats.compute_statistics()

    print('subtrees average infected:')
    print(stats.subtrees_average_infected)

    print('subtrees_infected_nodes_by_time:')
    print(stats.subtrees_infected_nodes_by_time)

    #plot_average_infection(stats.subtree_ratio_list, range(len(stats.subtree_ratio_list)))
    #plot_results(range(len(stats.subtree_ratio_list)), stats.subtrees_mean, stats.subtrees_lower_bound, stats.subtrees_upper_bound)
    
    #plot_average_infection(stats.centrality_average_infected, range(len(stats.centrality_average_infected)))
    #plot_results(range(len(stats.centrality_average_infected)), stats.centrality_average_infected, stats.centrality_lower_bound, stats.centrality_upper_bound)

    #plot_average_infection(stats.random_average_infected, range(len(stats.random_average_infected)))
    #plot_results(range(len(stats.random_average_infected)), stats.random_average_infected, stats.random_lower_bound, stats.random_upper_bound)

    plot_infections()

# note riunione
# per fare i confidence interval runnare x volte il main e salvare i risultati
# poi fare la media e varianza dei risultati
# salvare il numero di nodi finali infetti, numero di epoch totali, tempo di esecuzione
# fare un plot con la media e i confidence interval
# - cambiare il numero di rng per ogni algoritmo
