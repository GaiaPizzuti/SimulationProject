from copy import deepcopy
import sys
from temporalGraph import influence_maximization, spread_infection, get_random_seed_set
from subTreeInfection import subtrees_methods
from vsCentrality import centrality_analysis
from vsRandom import random_analysis
from comparison import result_comparison
from degreeNodes import degree_nodes
from cc import compare_cc
from settings import *
import numpy as np

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
        seed_set = influence_maximization(filename)
    
    #print('seed set:', seed_set)
    
    #print('\n\n---- simulate infection ----\n\n')
    test_seed_set = deepcopy(seed_set)
    infected = spread_infection(test_seed_set, filename)
    #print('number of infected nodes in the simulation:', infected)
    
    #print('\n\n---- minimize infection with subtrees ----\n\n')
    
    subtree, ratio = subtrees_methods(filename, set(seed_set), node_budget, prob_of_being_infected)
    
    """ print('\n\n---- minimize infection with centrality ----\n\n')
    
    centrality = centrality_analysis(filename, set(seed_set), node_budget, set(subtree), prob_of_being_infected)

    print('\n\n---- minimize infection with random ----\n\n')

    random = random_analysis(filename, set(seed_set), node_budget, prob_of_being_infected, set(subtree))
    
    print('\n\n---- result comparison ----\n\n')
    
    result_comparison(filename, set(seed_set), node_budget, set(subtree), set(centrality), set(random), prob_of_being_infected)
    
    degree_nodes(filename, subtree, centrality)
    
    compare_cc(filename, subtree, centrality) """
    
    return subtree, ratio

def plot_results(means, ratio_infection, lower_bounds, upper_bounds, confidence):
    """
    function to plot the ratio between the number of infected nodes after the attack and the number of infected nodes before the attack
    repeat the simulation times_main times

    Args:
        - means: the list of the means of the number of infected nodes
        - std_devs: the list of the standard deviations of the number of infected nodes
        - variances: the list of the variances of the number of infected nodes
        - ratio_infection: the list of the ratio of infection
    """

    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 5))
    #plt.plot(ratio_infection, label='ratio of infection')
    plt.plot(means, label='mean')
    # fill the area between the confidence intervals
    plt.fill_between(range(times_main), means - confidence, means + confidence, color='blue', alpha=0.1)
    plt.xlabel('time')
    plt.ylabel('ratio')
    plt.legend()
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
    means = []
    std_devs = []
    variances = []
    ratio_infection = []
    lower_bounds = []
    upper_bounds = []
    for time in range(times_main):
        print('time:', time)
        selected_nodes, ratio = adversarial_attack_at_influence_maximization()
        total_selected_nodes.append(selected_nodes)
        ratio_infection.append(ratio)

    
        #print('total selected nodes:')
        #for selected_nodes in total_selected_nodes:
            #print(selected_nodes)
        
        #print('---- end ----')

        # calculate the mean, the standard deviation and the variance of the ratio of infection
        mean = np.mean(ratio_infection)
        #print('mean ratio:', mean_ratio)
        variance = np.var(ratio_infection)
        #print('variance ratio:', variance_ratio)
        std_dev = np.std(ratio_infection)
        #print('standard devation ratio:', std_dev_ratio)

        means.append(mean)
        std_devs.append(std_dev)
        variances.append(variance)

        tstudent = 2.2010
        lb = mean - tstudent * np.sqrt(variance/len(ratio_infection))
        ub = mean + tstudent * np.sqrt(variance/len(ratio_infection))

        lower_bounds.append(lb)
        upper_bounds.append(ub)

    confidence = 1.96 * np.std(ratio_infection) / np.sqrt(times_main)
    print(f"CI: {confidence}")
    plot_results(means, ratio_infection, lower_bounds, upper_bounds, confidence)
