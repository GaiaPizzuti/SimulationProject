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
import time

filename = sys.argv[1]
node_budget = int(sys.argv[2])

def adversarial_attack_at_influence_maximization ():
    '''
    main function
    
    it is needed to call this function with:
        - argv[1]: the name of the relative file's path containing the graph to analyze (e.g. data/email.txt)
    '''
    
    #print('---- find seed set ----\n\n')
    
    if len(sys.argv) == 4:
        seedset_budget = int(sys.argv[3])
        seed_set = get_random_seed_set(filename, seedset_budget)
    else:
        seed_set = influence_maximization(filename) # type: ignore
    
    #print('seed set:', seed_set)
    
    #print('\n\n---- simulate infection ----\n\n')
    test_seed_set = deepcopy(seed_set)
    infected = spread_infection(test_seed_set, filename)
    #print('number of infected nodes in the simulation:', infected)
    
    #print('\n\n---- minimize infection with subtrees ----\n\n')
    
    #stats.simulation_type = "subtrees"
    subtree, subtree_mean = subtrees_methods(filename, set(seed_set), node_budget, prob_of_being_infected) # type: ignore
    
    #stats.simulation_type = "centrality"
    centrality, centrality_mean = centrality_analysis(filename, set(seed_set), node_budget, set(subtree), prob_of_being_infected) # type: ignore

    #stats.simulation_type = "random"
    random, random_mean = random_analysis(filename, set(seed_set), node_budget, prob_of_being_infected, set(subtree))

    #result_comparison(filename, set(seed_set), node_budget, set(subtree), set(centrality), set(random), prob_of_being_infected)
    
    #degree_nodes(filename, subtree, centrality)
    
    #compare_cc(filename, subtree, centrality)

    attack = [subtree, centrality, random]
    mean = [subtree_mean, centrality_mean, random_mean]
    
    return attack, mean

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
    plt.plot(time, mean, label='Mean')
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
    

    for i in range(times_main):
        rng = generators[i]
        
        # calculate the execution time
        starting_time = time.time()
        selected_nodes, mean_infected = adversarial_attack_at_influence_maximization()
        ending_time = time.time()

        execution_time = ending_time - starting_time
        stats.execution_times.append(execution_time)

        stats.subtrees_attack_set.append(selected_nodes[0])
        stats.centrality_attack_set.append(selected_nodes[1])
        stats.random_attack_set.append(selected_nodes[2])
    
        stats.mean_subtrees.append(mean_infected[0])
        stats.mean_centrality.append(mean_infected[1])
        stats.mean_random.append(mean_infected[2])

    # calculate the variance
    stats.variance_random = np.var(stats.mean_random)
    stats.variance_centrality = np.var(stats.mean_centrality)
    stats.variance_subtrees = np.var(stats.mean_subtrees)

    # calculate the standard deviation
    stats.std_random = np.std(stats.mean_random)
    stats.std_centrality = np.std(stats.mean_centrality)
    stats.std_subtrees = np.std(stats.mean_subtrees)

    stats.compute_statistics()

    def compute_confidence_interval(mean, std):
        x = len(mean)
        mean_overall = np.mean(mean)
        ci95 = 1.96 * (std / np.sqrt(x))  # 95% confidence interval

        lower_bound = mean_overall - ci95
        upper_bound = mean_overall + ci95
        
        return lower_bound, upper_bound
    
    stats.random_lower_bound, stats.random_upper_bound = compute_confidence_interval(stats.mean_random, stats.variance_random)
    stats.centrality_lower_bound, stats.centrality_upper_bound = compute_confidence_interval(stats.mean_centrality, stats.variance_centrality)
    stats.subtrees_lower_bound, stats.subtrees_upper_bound = compute_confidence_interval(stats.mean_subtrees, stats.variance_subtrees)

    plot_infections()

    # plot the results
    time = list(range(1, len(stats.mean_random) + 1))
    plot_results(time, stats.mean_random, stats.random_lower_bound, stats.random_upper_bound, np.mean(stats.mean_random))
    time = list(range(1, len(stats.mean_centrality) + 1))
    plot_results(time, stats.mean_centrality, stats.centrality_lower_bound, stats.centrality_upper_bound, np.mean(stats.mean_centrality))
    time = list(range(1, len(stats.mean_subtrees) + 1))
    plot_results(time, stats.mean_subtrees, stats.subtrees_lower_bound, stats.subtrees_upper_bound, np.mean(stats.mean_subtrees))

    # print the average execution time
    print(f'Average execution time: {np.mean(stats.execution_times)} seconds')

    # print the overall mean and variance
    print(f'Overall mean random: {np.mean(stats.mean_random)}, variance: {stats.variance_random}')
    print(f'Overall mean centrality: {np.mean(stats.mean_centrality)}, variance: {stats.variance_centrality}')
    print(f'Overall mean subtrees: {np.mean(stats.mean_subtrees)}, variance: {stats.variance_subtrees}')


# note riunione
# per fare i confidence interval runnare x volte il main e salvare i risultati
# poi fare la media e varianza dei risultati
# salvare il numero di nodi finali infetti, numero di epoch totali, tempo di esecuzione
# fare un plot con la media e i confidence interval
# - cambiare il numero di rng per ogni algoritmo
