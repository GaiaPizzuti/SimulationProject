# Simulation and Output Analysis of Adversarial Attack at Influence Maximization in Graphs

This project analyzes the performances of three algorithms designed to attack an adversarial influence maximization algorithm on both static and temporal networks.

The spread of viruses (or information, rumors, and malware) in networks is a critical problem in epidemiology, cybersecurity, and social network analysis.  
This project aims to compare different mitigation strategies and understand how algorithmic choices impact the containment of a virus within a network.

## Algorithms Evaluated
The following algorithms have been implemented and evaluated:

- Random nodes selection: nodes for the attack set are randomly selected

- Centrality nodes selection: nodes for the attack set are selected based on the number of connections they have

- Subtree nodes selection: nodes for the attack set are selected based on their infection subtree's dimension

## Features
- Simulation of the virus spread with Influence Maximization on mind

- Implementation of the three algorithms 

- Simulation of the virus spread after the algorithms' action, adding an attack set

- Collection on algorithms' performance

- Output analysis and plotting


## Requirments
- Python 3.9
- numpy
- matplotlib
- igraph
- scipy

## Installation
1. Clone the repositories ```bash https://github.com/GaiaPizzuti/SimulationProject.git ``` 

2. Navigate the repository ```cd SimulationProject```

3. (Recommended) Create a virtual environment ```python3 -m venv .venv```

4. (Recommended) Activate the virtual environment ```source .venv/bin/activate```

5. Install the dependences ```pip install -r utils/requirements.txt```

6. Run the project ```python main.py <filename> <attackset_budget> [<seedset_budget> | <times_main> <times_infection> <prob_of_being_infected>]```    

## Project Structure

```
.
├── data/
├── output/
├── src/
│   ├── cc.py
│   └── inferctionSimulation.py
│   └── main.py
│   └── settings.py
│   └── statistics.py
│   └── subTreeInfection.py
│   └── temporalGraph.py
│   └── vsCentrality.py
│   └── vsRandom.py
├── utils/
│   ├── convert.py
│   ├── generate.py
│   └── requirements.txt
├── .gitignore
├── run_batches.py
└── README.md

```

## Experiment Settings
Settings can be found under src/settings.py and can be modified to observe different results. The variables are the following:
```
DEBUG = False                                 //debug mode, True enables it, False disables it
prob_of_being_infected = 0.8                  //probability of infection            
times_main = 10                               //times the whole experiment is run
times_infection = 10                          //times each infection simulation (no attack set/algorithm/graph minus attack set) is run

# High quality initial entropy
entropy = 0x87351080e25cb0fad77a44a3be03b491  //entropy for NumPy's PCG64 BitGenerator
```

## Output
The program will output in the stream text results. A plot will be saved in the output folder, detailing the experiment's settings. An example is showcased below.
```
running python src/main.py data/cliques_less_bridges.txt 5 10 1 0.2:

--------------- Influence Spread statistics with the different methods ---------------
subtrees mean, variance, lower bound and upper bound:
19.6 64.26666666666667 13.865234530577657 25.334765469422344
centrality mean, variance, lower bound and upper bound:
13.2 30.62222222222221 9.241404505359395 17.158595494640604
random mean, variance, lower bound and upper bound:
16.2 60.17777777777776 10.650666222217641 21.749333777782358

---- Improvement in graph resistance with the different methods (lower is better) ----
Subtree improvement: 1.0546753246753247
Centrality improvement: 0.8373351158645276
Random improvement: 0.954607843137255
```
<img width="1000" height="600" alt="plot_cliques_less_bridges_1_10_0_2" src="https://github.com/user-attachments/assets/e17ebee6-3156-4018-aa64-b57907ddbafc" />

