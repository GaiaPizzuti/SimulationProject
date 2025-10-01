#!/bin/bash

# simulation_venv/bin/python src/main.py data/ring.txt 3 > output.txt

DATASET_LIST=(
#"data/as19971108-new.txt"
#"data/cit-HepPh-pruned-new.txt"
"data/cliques_less_bridges.txt"
#"data/CollegeMsg.txt"
#"data/email-Eu-core-temporal-Dept2.txt"
#"data/fb-forum.txt"
"data/ring.txt"
)

DATASET_NAMES=(
#"as19971108-new"
#"cit-HepPh-pruned-new"
"cliques_less_bridges"
#"CollegeMsg"
#"email-Eu-core-temporal-Dept2"
#"fb-forum"
"ring"
)

DATASET_SEEDSET_BUDGETS=(
    #1 350 700
    #1 7 15
    1 2 5
    #1 25 50
    #1 80 160
    #1 7 15
    1 40 80
)

# For each dataset, run the simulation with the three associated seedset budgets
for i in {0..1}
do
    for j in {0..2}
    do
        echo "Running simulation for ${DATASET_LIST[i]} with seedset budget ${DATASET_SEEDSET_BUDGETS[i*3+j]}"
        simulation_venv/bin/python src/main.py ${DATASET_LIST[i]} ${DATASET_SEEDSET_BUDGETS[i*3+j]} > output_${DATASET_NAMES[i]}_${DATASET_SEEDSET_BUDGETS[i*3+j]}.txt
    done
done

