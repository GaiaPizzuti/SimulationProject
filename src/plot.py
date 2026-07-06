import matplotlib.pyplot as plt
import numpy as np
from settings import DEBUG, prob_of_being_infected, times_main, times_infection, filename_dict
from statistics import stats

def plot_infections(filename):
    '''
    function to plot the total number of infected nodes for each method (subtree, centrality, random) as a function of the number of independent replications, with the upper and lower bounds of the confidence interval as errors in a bar chart
    '''
    plt.figure(figsize=(10, 6))
    
    x = np.arange(len(stats.subtrees_sample_means_array))
    width = 0.25

    plt.bar(x - width, stats.subtrees_sample_means_array, width, label='Subtree', capsize=5)
    plt.bar(x, stats.centrality_sample_means_array, width, label='Centrality', capsize=5)
    plt.bar(x + width, stats.random_sample_means_array, width, label='Random', capsize=5)

    # set errorbar colors to be darker than the bar colors
    plt.errorbar(x - width, stats.subtrees_sample_means_array, yerr=(stats.subtrees_upper_bound - stats.subtrees_lower_bound) / 2, fmt='none', ecolor='#0800a8', capsize=5)
    plt.errorbar(x, stats.centrality_sample_means_array, yerr=(stats.centrality_upper_bound - stats.centrality_lower_bound) / 2, fmt='none', ecolor='#994900', capsize=5)
    plt.errorbar(x + width, stats.random_sample_means_array, yerr=(stats.random_upper_bound - stats.random_lower_bound) / 2, fmt='none', ecolor='#3f6e42', capsize=5)

    plt.axline((-0.5, stats.subtrees_grand_mean), (len(stats.subtrees_sample_means_array) - 0.5, stats.subtrees_grand_mean), color='#0800a8', linestyle='--', label='Subtree Mean', alpha=0.3)
    plt.axline((-0.5, stats.centrality_grand_mean), (len(stats.centrality_sample_means_array) - 0.5, stats.centrality_grand_mean), color='#994900', linestyle='--', label='Centrality Mean', alpha=0.3)
    plt.axline((-0.5, stats.random_grand_mean), (len(stats.random_sample_means_array) - 0.5, stats.random_grand_mean), color='#3f6e42', linestyle='--', label='Random Mean', alpha=0.3)

    plt.xlabel('Independent Replications')
    plt.ylabel('Average Total Infected Nodes')
    plt.xticks(x, [f'IR {i+1}' for i in range(len(stats.subtrees_sample_means_array))])
    plt.legend()    
    plt.grid()

    filename_short = filename.split('/')[-1].split('.')[0]
    prob = str(prob_of_being_infected).replace('.', '_')
    plt.title('Average Total Infected Nodes with CIs, file: ' + filename_short + ', t_main: ' + str(times_main) + ', t_infection: ' + str(times_infection) + ', p: ' + str(prob_of_being_infected) )
    plt.ylim(0, filename_dict[filename_short] + 10)  # Set y-axis limit based on the number of nodes in the graph
    plt.savefig(f'output/plot_{filename_short}_{times_infection}_{times_main}_{prob}.png')
    print(f'Plot saved as output/plot_{filename_short}_{times_infection}_{times_main}_{prob}.png')

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