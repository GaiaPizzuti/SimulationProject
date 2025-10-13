from numpy.random import Generator, PCG64, SeedSequence
import sys

prob_of_being_infected = 0.3
times_main = 5
times = 1

# High quality initial entropy
entropy = 0x87351080e25cb0fad77a44a3be03b491
base_seq = SeedSequence(entropy)
child_seqs = base_seq.spawn(times_main * times)    # a list of 10 SeedSequences
# print(seq for seq in child_seqs)
generators = [Generator(PCG64(seq)) for seq in child_seqs]

rng = generators[0]

if len(sys.argv) == 5:
    times_main = int(sys.argv[3])
    times = int(sys.argv[4])
    print(f'Setting times_main to {times_main} and times to {times} from command line arguments.')
    # regenerate the random number generators with the new times_main and times
    base_seq = SeedSequence(entropy)
    child_seqs = base_seq.spawn(times_main * times)    # a list of times
    generators = [Generator(PCG64(seq)) for seq in child_seqs]
    rng = generators[0]