# ------------------------- Settings -------------------------
# These values define the default settings for the simulation. They can be overridden by command line arguments when running the main.py script.
# DEBUG: sets debug mode if True, printing additional information during execution
# CONFIDENCE_INTERVAL: sets the confidence interval for output analysis
# prob_of_being_infected: sets the probability of a node getting infected during the simulation
# times_main: sets the number of independent replications of the simulation
# times_infection: sets the number of infection simulations to run in each IR

from numpy.random import Generator, PCG64, SeedSequence
import sys

DEBUG = True
CONFIDENCE_INTERVAL = 0.95
prob_of_being_infected = 0.8
times_main = 10
times_infection = 10

filename_dict = {
    "as19971108-new": 3015,
    "cit-HepPh-pruned-new": 172,
    "cliques_less_bridges": 43,
    "CollegeMsg": 1899,
    "email-Eu-core-temporal-Dept2": 171,
    "fb-forum": 899,
    "ring": 499,
}

# create the generators given a starting entropy
entropy = 0x87351080e25cb0fad77a44a3be03b491
base_seq = SeedSequence(entropy)
child_seqs = base_seq.spawn(times_main)
generators = [Generator(PCG64(seq)) for seq in child_seqs]

rng = generators[0]

# if provided, override the default settings with command line arguments
if len(sys.argv) == 6:
    times_main = int(sys.argv[3])
    times_infection = int(sys.argv[4])
    prob_of_being_infected = float(sys.argv[5])

    # validate the input parameters
    if times_main <= 0 or times_infection <= 0 or prob_of_being_infected < 0 or prob_of_being_infected > 1:
        print("Error: times_main and times_infection must be positive integers, and prob_of_being_infected must be a float between 0 and 1.")
        sys.exit(1)

    if(DEBUG): print(f'Setting t_main to {times_main}, t_infection to {times_infection} and p to {prob_of_being_infected} from command line arguments.')

    # Generate new random number generators for each Independent Replication
    base_seq = SeedSequence(entropy)
    child_seqs = base_seq.spawn(times_main)
    generators = [Generator(PCG64(seq)) for seq in child_seqs]
    rng = generators[0]