import numpy as np
from scipy.stats import norm, t

class Statistics:
    def __init__(self):
        self.simulation_type = ""
        self.subtrees_attack_set = []
        self.centrality_attack_set = []
        self.random_attack_set = []

        self.current_infected_nodes = []
        self.subtrees_infected_nodes_by_time = []
        self.centrality_infected_nodes_by_time = []
        self.random_infected_nodes_by_time = []

    def save_infected_nodes_list(self):
        if self.simulation_type == "subtrees":
            self.subtrees_infected_nodes_by_time.append(self.current_infected_nodes)
        elif self.simulation_type == "centrality":
            self.centrality_infected_nodes_by_time.append(self.current_infected_nodes)
        elif self.simulation_type == "random":
            self.random_infected_nodes_by_time.append(self.current_infected_nodes)
        self.current_infected_nodes = []
    
    def compute_statistics(self):
        def compute_average(infected_nodes_by_time):
            min_length = min(len(lst) for lst in infected_nodes_by_time)
            # return list of average infected nodes at each time
            return [sum(lst[i] for lst in infected_nodes_by_time) / len(infected_nodes_by_time) for i in range(min_length)]

        self.subtrees_average_infected = compute_average(self.subtrees_infected_nodes_by_time)
        self.centrality_average_infected = compute_average(self.centrality_infected_nodes_by_time)
        self.random_average_infected = compute_average(self.random_infected_nodes_by_time)

        CONFIDENCE_INTERVAL = 0.95
        z = norm.ppf(1 - (1 - CONFIDENCE_INTERVAL) / 2)
        def compute_variance(average_infected):
            mean = []
            variance = []
            lower_bound = []
            upper_bound = []
            infections_at_time = []
            LENGTH = len(average_infected)
            for index in range(len(average_infected)):
                infections_at_time.append(average_infected[index])
                grand_mean = np.mean(average_infected)
                mean.append(grand_mean)

                variance_curr = 0
                for i in range(len(average_infected)):
                    variance_curr = variance_curr + ((average_infected[i] - grand_mean)**2)
                variance_curr *= 1/(len(average_infected) - 1)

                t_student = t.ppf(1 - (1 - CONFIDENCE_INTERVAL) / 2, LENGTH - 1)
                # print("t_student value:", t_student, "for", LENGTH - 1, "degrees of freedom", "and confidence interval", CONFIDENCE_INTERVAL)

                # variance.append(np.var(average_infected))
                variance.append(variance_curr)

                std_dev_speed = np.sqrt(variance[-1])
                margin_error = z * std_dev_speed / np.sqrt(LENGTH)

                lb0 = grand_mean - t_student * np.sqrt(variance_curr/LENGTH)
                ub0 = grand_mean + t_student * np.sqrt(variance_curr/LENGTH)

                # lower_bound.append(mean[-1] - margin_error)
                # upper_bound.append(mean[-1] + margin_error)
                lower_bound.append(lb0)
                upper_bound.append(ub0)

            return infections_at_time, mean, variance, lower_bound, upper_bound
            
        # compute ratio between the two methods
        #self.ratio_list = [self.subtrees_average_infected[i] / self.centrality_average_infected[i] for i in range(min(len(self.subtrees_average_infected), len(self.centrality_average_infected)))]
        #self.subtrees_infected_nodes_by_time, self.subtrees_mean, self.subtrees_variance, self.subtrees_lower_bound, self.subtrees_upper_bound = compute_variance(self.ratio_list)
        
        self.subtrees_infected_nodes_by_time, self.subtrees_mean, self.subtrees_variance, self.subtrees_lower_bound, self.subtrees_upper_bound = compute_variance(self.subtrees_average_infected)
        self.centrality_infected_nodes_by_time, self.centrality_mean, self.centrality_variance, self.centrality_lower_bound, self.centrality_upper_bound = compute_variance(self.centrality_average_infected)
        self.random_infected_nodes_by_time, self.random_mean, self.random_variance, self.random_lower_bound, self.random_upper_bound = compute_variance(self.random_average_infected)



stats = Statistics()