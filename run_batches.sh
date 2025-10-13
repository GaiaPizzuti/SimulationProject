#!/bin/bash

# simulation_venv/bin/python src/main.py data/ring.txt 3 > output.txt

DATASET_LIST=(
#"data/as19971108-new.txt"
#"data/cit-HepPh-pruned-new.txt"
"data/cliques_less_bridges.txt"
#"data/CollegeMsg.txt"
"data/email-Eu-core-temporal-Dept2.txt"
#"data/fb-forum.txt"
"data/ring.txt"
)

DATASET_NAMES=(
#"as19971108-new"
#"cit-HepPh-pruned-new"
"cliques_less_bridges"
#"CollegeMsg"
"email-Eu-core-temporal-Dept2"
#"fb-forum"
"ring"
)

DATASET_NODE_BUDGETS=(
    #1 350 700
    #1 7 15
    1 2 2
    #1 25 50
    1 10 10
    #1 7 15
    1 15 15
)

DATASET_TIMES_MAIN=(
    #10 10 10
    #10 10 10
    10 10 100
    #10 10 10
    10 10 100
    #10 10 10
    10 10 100
)

DATASET_NO_SIMULATION_PER_RUN=(
    #10 10 10
    #10 10 10
    10 10 10
    #10 10 10
    10 10 10
    #10 10 10
    10 10 10
)

# For each dataset, run the simulation with the three associated seedset budgets
for i in {0..1}
do
    for j in {0..2}
    do
        echo "Running simulation for ${DATASET_LIST[i]} with seedset budget ${DATASET_NODE_BUDGETS[i*3+j]} (times_main=${DATASET_TIMES_MAIN[i*3+j]}, no_simulations_per_run=${DATASET_NO_SIMULATION_PER_RUN[i*3+j]})"
        simulation_venv/bin/python src/main.py ${DATASET_LIST[i]} ${DATASET_NODE_BUDGETS[i*3+j]} ${DATASET_TIMES_MAIN[i*3+j]} ${DATASET_NO_SIMULATION_PER_RUN[i*3+j]} > output2/output_${DATASET_NAMES[i]}_nodebudget${DATASET_NODE_BUDGETS[i*3+j]}_timesmain${DATASET_TIMES_MAIN[i*3+j]}_times${DATASET_NO_SIMULATION_PER_RUN[i*3+j]}.txt
    done
done

