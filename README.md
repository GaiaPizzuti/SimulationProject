# AttackOnTemporalNetwork

The project analyze the performances of three algorithm designed to attack an adversarial influence maximization algorithms on both static and temporal networks.

The spread of viruses (or information, rumors, or malware) in networks is a critical problem in epidemiology, cybersecurity, and social network analysis.  
This project aims to compare different mitigation strategies and understand how algorithmic choices impact the containment of a virus within a network.

## Algorithms Evaluated
The following algorithms have been implemented and evaluated:
1 - Random nodes selection: nodes are randomly selected
2 - Centrality nodes selection: nodes are selected based on the number of connections they have
3 - Subtree nodes selection: nodes are selected based on their subtree's dimension

## Features
1 - Simulation of the virus spread
2 - Implementation of the three algorithms
3 - Simulation of the virus spread after the algorithms' action
4 - Algorithms evaluation
5 - Simulation of algorithms' performance

## Requirments
- Python 3.9
- numpy
- matplotlib
- igraph

## Installation
1 - Clone the repositories ```bash https://github.com/GaiaPizzuti/SimulationProject.git ``` 
2 - Navigate the repository ```cd SimulationProject```
3 - Install the dependences ```pip install -r requirements.txt```
4 - Run the project ```python main.py```

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
