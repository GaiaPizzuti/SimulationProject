import os
import sys
import time
import datetime
import random

def generate_tree(filepath):
    old_file = open("/home/luca.cavalcanti/simulation/data/cit-HepPh-dates.txt", 'r')
    old_file2 = open("/home/luca.cavalcanti/simulation/data/cit-HepPh.txt", 'r')
    new_file = open(filepath, "w")
    
    old_dataset = old_file2.readlines()
    dates = old_file.readlines()
    nodes_to_save = []

    for line in dates:
        date = line.split()[0]
        nodes_to_save.append(date)

    print(nodes_to_save)

    old_dataset = old_dataset[4:]

    for line in old_dataset:
        split = line.split()
        src = split[0]
        dst = split[1]

        if src in nodes_to_save and dst in nodes_to_save:
            new_file.write(dst + " " + src + "\n")

def generate_ring(filepath):
    new_file = open("../../data/ring.txt", "w")
    node_counter = 0
    for _ in range(1,500):
        new_file.write(str(node_counter - 1) + " " + str(node_counter) + " 0\n") 
        node_counter = node_counter + 1
    
    new_file.write(str(node_counter) + " 0 " + "\n") 

def generate_clique(filepath):
    new_file = open("../../data/clique.txt", "w")
    max_nodes_per_clique = 15
    min_nodes_per_clique = 5
    max_bridges = 3
    min_bridges = 1
    cliques = 4

    clique_nodes_arr = []

    node_counter = 0

    for clique in range(cliques):
        clique_nodes = random.randint(min_nodes_per_clique, max_nodes_per_clique)
        clique_nodes_arr.append((node_counter, node_counter+clique_nodes-1))

        # print clique
        for src in range(clique_nodes):
            for dst in range(clique_nodes):
                if src != dst:
                    new_file.write(str(node_counter + src) + " " + str(node_counter + dst) + " 0 \n")
        
        node_counter += clique_nodes

    bridge_str = []
    # connect cliques
    for src_cl in range(cliques):
        for dst_cl in range(cliques):
            if src_cl != dst_cl:
                bridges = random.randint(min_bridges, max_bridges)
                for bridge in range(bridges):
                    src = random.randint(clique_nodes_arr[src_cl][0], clique_nodes_arr[src_cl][1])
                    dst = random.randint(clique_nodes_arr[dst_cl][0], clique_nodes_arr[dst_cl][1])

                    new_str = str(src) + " " + str(dst) + " 0\n"

                    if new_str not in bridge_str:
                        new_file.write(new_str)
                        bridge_str.append(new_str)




generate_clique("../../data/tree2.txt")