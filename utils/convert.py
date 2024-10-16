import os
import sys
import time
import datetime

def convert(filepath):
    old_file = open(filepath, 'r')
    new_file = open(filepath[:-4]+'-new.txt', "w")

    lines = old_file.readlines()
    old_file.close()

    nodes = {}
    node_counter = 0
    # n_edges = int(lines[0].split()[1])
    # lines = lines[1:n_edges+1]
    for line in lines:
        values = line.split()
        src = values[0]
        dst = values[1]

        src_id, dst_id = 0, 0

        # timestamp = values[3] + " " + values[4]

        if src in nodes.keys():
            src_id = nodes[src]
        else:
            src_id = node_counter
            node_counter += 1
            nodes[src] = src_id

        if dst in nodes.keys():
            dst_id = nodes[dst]
        else:
            dst_id = node_counter
            node_counter += 1
            nodes[dst] = dst_id

        # d = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        # unixtime = time.mktime(d.timetuple())

        # new_file.write(str(src_id) + " " + str(dst_id) + " " + str(int(unixtime)) + "\n")

        new_file.write(str(src_id) + " " + str(dst_id) + " " + "0" + "\n")

            

convert("/home/luca.cavalcanti/simulation/SimulationProject/data/cit-HepPh-pruned.txt")
# convert("../../data/8m.txt")