# ------------------------- Statistics -------------------------
# Module containing class and methods to collect observations and perform output analysis

import numpy as np
from scipy.stats import norm, t
from settings import *

def compute_sample_means_array(total_infected_nodes):
    '''Computes the sample means of the total infected nodes for each independent replication.'''
    sample_means_array = []
    for i in range(len(total_infected_nodes)):
        sample_means_array.append(np.mean(total_infected_nodes[i]))
    return sample_means_array

def compute_independent_replications_estimators(sample_means_array):
    '''Computes the simulation estimators given the sample means.'''
    grand_mean = 0
    variance = 0
    lower_bound = 0
    upper_bound = 0

    LENGTH = len(sample_means_array)
    grand_mean = np.mean(sample_means_array)

    variance_curr = 0
    for i in range(len(sample_means_array)):
        variance_curr = variance_curr + ((sample_means_array[i] - grand_mean)**2)
    variance_curr *= 1/(len(sample_means_array) - 1)

    variance = variance_curr
    t_student = t.ppf(1 - (1 - CONFIDENCE_INTERVAL) / 2, df=LENGTH - 1)

    lower_bound = grand_mean - t_student * np.sqrt(variance/LENGTH)
    upper_bound = grand_mean + t_student * np.sqrt(variance/LENGTH)

    return grand_mean, variance, lower_bound, upper_bound

class Statistics:
    def __init__(self):
        self.naive_total_infected_nodes = []
        self.subtrees_total_infected_nodes = []
        self.centrality_total_infected_nodes = []
        self.random_total_infected_nodes = []

        self.subtrees_sample_means_array = []
        self.subtrees_grand_mean = 0
        self.subtrees_variance = 0
        self.subtrees_lower_bound = 0
        self.subtrees_upper_bound = 0
   
        self.centrality_sample_means_array = []
        self.centrality_grand_mean = 0
        self.centrality_variance = 0
        self.centrality_lower_bound = 0
        self.centrality_upper_bound = 0
 
        self.random_sample_means_array = []
        self.random_grand_mean = 0     
        self.random_variance = 0
        self.random_lower_bound = 0
        self.random_upper_bound = 0

        self.naive_grand_mean = 0

        self.improvement_subtree = list()
        self.improvement_centrality = list()
        self.improvement_random = list()

    def output_analysis(self):
        '''Computes the grand mean, variance, and confidence intervals for the total infected nodes for each method, starting from the recorded observations.'''
        # first, compute each Replication's mean
        self.subtrees_sample_means_array = compute_sample_means_array(self.subtrees_total_infected_nodes)
        self.centrality_sample_means_array = compute_sample_means_array(self.centrality_total_infected_nodes)
        self.random_sample_means_array = compute_sample_means_array(self.random_total_infected_nodes)
        self.naive_sample_means_array = compute_sample_means_array(self.naive_total_infected_nodes)
        
        # then use the Replications' means to compute the grand mean, variance, and confidence intervals
        self.subtrees_grand_mean, self.subtrees_variance, self.subtrees_lower_bound, self.subtrees_upper_bound = compute_independent_replications_estimators(self.subtrees_sample_means_array)
        self.centrality_grand_mean, self.centrality_variance, self.centrality_lower_bound, self.centrality_upper_bound = compute_independent_replications_estimators(self.centrality_sample_means_array)
        self.random_grand_mean, self.random_variance, self.random_lower_bound, self.random_upper_bound = compute_independent_replications_estimators(self.random_sample_means_array)
        self.naive_grand_mean, _, _, _ = compute_independent_replications_estimators(self.naive_sample_means_array)

        # finally, use the Replications' means to compute the ratio of infected nodes between the simulation after the algorithm and before
        self.improvement_subtree = [self.subtrees_sample_means_array[i] / self.naive_sample_means_array[i] for i in range(len(self.subtrees_sample_means_array))]
        self.improvement_centrality = [self.centrality_sample_means_array[i] / self.naive_sample_means_array[i] for i in range(len(self.centrality_sample_means_array))]
        self.improvement_random = [self.random_sample_means_array[i] / self.naive_sample_means_array[i] for i in range(len(self.random_sample_means_array))]


stats = Statistics()