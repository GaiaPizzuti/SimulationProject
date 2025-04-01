from numpy.random import Generator, PCG64, SeedSequence

prob_of_being_infected = 0.2
times_main = 1
times = 10

# High quality initial entropy
entropy = 0x87351080e25cb0fad77a44a3be03b491
base_seq = SeedSequence(entropy)
child_seqs = base_seq.spawn(times_main)    # a list of 10 SeedSequences
# print(seq for seq in child_seqs)
generators = [Generator(PCG64(seq)) for seq in child_seqs]

rng = generators[0]