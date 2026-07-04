# AttackOnTemporalNetwork

This project analyzes the performances of three algorithms designed to attack an adversarial influence maximization algorithm on both static and temporal networks.

The spread of viruses (or information, rumors, and malware) in networks is a critical problem in epidemiology, cybersecurity, and social network analysis.  
This project aims to compare different mitigation strategies and understand how algorithmic choices impact the containment of a virus within a network.

## Algorithms Evaluated
The following algorithms have been implemented and evaluated:

- Random nodes selection: nodes for the attack set are randomly selected

- Centrality nodes selection: nodes for the attack set are selected based on the number of connections they have

- Subtree nodes selection: nodes for the attack set are selected based on their infection subtree's dimension

## Features
- Simulation of the virus spread

- Implementation of the three algorithms

- Simulation of the virus spread after the algorithms' action

- Algorithms' evaluation

- Simulation of algorithms' performance


## Requirments
- Python 3.9
- numpy
- matplotlib
- igraph

## Installation
1. Clone the repositories ```bash https://github.com/GaiaPizzuti/SimulationProject.git ``` 

2. Navigate the repository ```cd SimulationProject```

3. Install the dependences ```pip install -r requirements.txt```

4. Run the project ```python main.py [DATASET_PATH] [DATASET_SEEDSET_BUDGET]```

## Project Structure

```
.
├── data/
├── output/
├── src/
│   ├── cc.py
│   ├── comparison.py
│   ├── degreeNodes.py
│   └── inferctionSimulation.py
│   └── main.py
│   └── plot.py
│   └── settings.py
│   └── statistics.py
│   └── subTreeInfection.py
│   └── temporalGraph.py
│   └── vsCentrality.py
│   └── vsRandom.py
├── utils/
│   ├── convert.py
│   └── generate.py
├── representTemporalGraphs.py
├── run_batches.py
└── README.md

```

## Experiment Settings
Settings can be found under src/settings.py and can be modified to observe different results. The variables are the following:
```
prob_of_being_infected = 0.8                  //probability of infection            
times_main = 10                               //times the whole experiment is run
times = 10                                    //times each infection simulation (no attack set, algorithm, graph minus attack set) is run

# High quality initial entropy
entropy = 0x87351080e25cb0fad77a44a3be03b491  //entropy for NumPy's PCG64 BitGenerator
```

## Output
The program will output in the stream text results. A plot will be saved in the output folder, detailing the experiment's settings. An example is showcased below.

<img width="640" height="480" alt="plot_fb-forum_nodebudget80_timesmain10_times10" src="https://github.com/user-attachments/assets/fbe0a006-d268-420a-b83b-174d402d5405" />
