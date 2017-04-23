#!/usr/bin/env python3
#
# Copyright 2017 Philipp Winter <phw@nymity.ch>

import os
import sys
import random
import binascii

"""
What's the probability of NUM_BAD_HSDIRS nodes camping at least
CAMP_THRESHOLD replicas of a hidden service? Figure this out with a monte carlo
approach.
"""

# Number of monte carlo simulations
NUM_SIMULATIONS = 1000000

# Number of HSDir relays introduced in the network
NUM_BAD_HSDIRS = 6
# Number of replicas/descriptor-ids per hidden service
NUM_REPLICAS = 6

# The number of hex chars we want to match
CHARS_TO_MATCH = 2

# Number of replicas we want to camp
CAMP_THRESHOLD = 2

def simulate_hsdirs(iteration):
    """
    One round of the simulation:
    Generate new HSDirs and replicas and see how many prefixes we match.
    """

    r1 = r2 = False
    # Get some fresh randomness for this test run
    hsdirs = [binascii.hexlify(os.urandom(20)) for i in range(NUM_BAD_HSDIRS)]
    replicas  = [binascii.hexlify(os.urandom(20)) for i in range(NUM_REPLICAS)]

    # This is the results list. Each element of the list tells us whether we
    # managed to camp that replica.
    hits = [False] * NUM_REPLICAS

    # For each HSDir, go through the replicas, and see if any of them were camped.
    for hsdir in hsdirs:
        for i, replica in enumerate(replicas):
            if hsdir[:CHARS_TO_MATCH] == replica[:CHARS_TO_MATCH]:
                hits[i] = True

    # Check how many replicas were camped
    n_hits = 0
    for hit in hits:
        if hit == True:
            n_hits += 1

    # Did we camp enough replicas?
    return n_hits >= CAMP_THRESHOLD

def monte_carlo():
    """
    What's the probability of NUM_BAD_HSDIRS nodes camping at least
    CAMP_THRESHOLD replicas of a hidden service?
    """

    n_successes = 0

    for i in xrange(NUM_SIMULATIONS):
        success = simulate_hsdirs(i)
        if success:
            n_successes += 1

    print "=" * 80
    print "Results for shared_chars = %d, num_bad_hsdirs = %d, num_simulations = %d" % (CHARS_TO_MATCH, NUM_BAD_HSDIRS, NUM_SIMULATIONS)
    print "Successes %d out of %d" % (n_successes, NUM_SIMULATIONS)
    print "P(X>=%d) = %s" % (CAMP_THRESHOLD, str(n_successes/float(NUM_SIMULATIONS)))

def main():
    # Go through the simulation over and over.
    while True:
        monte_carlo()

if __name__ == "__main__":
    try:
        r = main()
        sys.exit(r)
    except KeyboardInterrupt:
        pass
