#!/bin/bash

DATASET_LIST=(
"data/as19971108-new.txt"
"data/cit-HepPh-pruned-new.txt"
"data/cliques_less_bridges.txt"
"data/CollegeMsg.txt"
"data/email-Eu-core-temporal-Dept2.txt"
"data/fb-forum.txt"
#"data/ring.txt"
)

DATASET_NAMES=(
"as19971108-new"
"cit-HepPh-pruned-new"
"cliques_less_bridges"
"CollegeMsg"
"email-Eu-core-temporal-Dept2"
"fb-forum"
#"ring"
)

DATASET_NODE_BUDGETS=(
    300 300
    17 17
    4 4
    190 190
    17 17
    90 90
#    50 50
)

DATASET_TIMES_MAIN=(
    10 10
    10 10
    10 10
    10 10
    10 10
    10 10
#    10 10
)

DATASET_NO_SIMULATION_PER_RUN=(
    10 100
    10 100
    10 100
    10 100
    10 100
    10 100
#    10 100
)

# For each dataset, run the simulation with the three associated attackset budgets
for i in {0..5}
do
    for j in {0..1}
    do
        for probability in 0.2 0.4 0.8
            do
                echo "Running simulation for ${DATASET_LIST[i]} with attackset budget ${DATASET_NODE_BUDGETS[i*2+j]}, times_main=${DATASET_TIMES_MAIN[i*2+j]}, t_infection=${DATASET_NO_SIMULATION_PER_RUN[i*2+j]}, probability=${probability}"
                python src/main.py ${DATASET_LIST[i]} ${DATASET_NODE_BUDGETS[i*2+j]} ${DATASET_TIMES_MAIN[i*2+j]} ${DATASET_NO_SIMULATION_PER_RUN[i*2+j]} $probability > output/output_${DATASET_NAMES[i]}_attackset${DATASET_NODE_BUDGETS[i*2+j]}_tmain${DATASET_TIMES_MAIN[i*2+j]}_tinfection${DATASET_NO_SIMULATION_PER_RUN[i*2+j]}_p${probability}.txt
            done
    done
done

