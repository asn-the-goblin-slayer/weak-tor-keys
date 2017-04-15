"""
This code is dealing with the following scenario:

Scenario: We just found in the Tor network N HSDir nodes that are related to
          each other, and some of them camp the descriptor-ids of a particular
          hidden service.

Question: What's the probability that N innocent relays would camp multiple
          descriptor-ids of a single hidden service?

Notes:    Every onion service has 6 responsible HSDirs (i.e. descriptor-ids).

          We say that a relay is camping the descriptor-id of a hidden service,
          if the relay's identity key matches the descriptor-id in its first 20
          bits. Since both the identity key and the descriptor-id are normally
          uniformly random strings, the probability of this prefix match
          happening is PREFIX_MATCH_PROB.

Approach: We can calculate the probability using the binomial disitribution, if
          we model the problem as such:

          How many heads do we get, if we flip a biased coin NUM_BAD_HSDIRS
          times, and the coin is biased with probability PREFIX_MATCH_PROB?
          Each coin flip represents the chance that an HSDir relay with a
          random identity key camps the descriptor-id of the hidden service.

          We use the binomial distribution with n=NUM_BAD_HSDIRS and
          p=PREFIX_MATCH_PROB.
"""

import scipy.stats

# Prob to match 5 hex chars ( = 20 bits)
PREFIX_MATCH_PROB = 1/float(pow(2,20))
# How many nodes we introduce to the network
NUM_BAD_HSDIRS = 6

# Get the binomial distr with n=NUM_BAD_HSDIRS and p=PREFIX_MATCH_PROB
rv = scipy.stats.binom(NUM_BAD_HSDIRS, PREFIX_MATCH_PROB)

# The binomial distribution can count how many descriptor-ids we accidentally
# camp if we introduce NUM_BAD_HSDIRS to the network.
# Or in other words: How many heads we get, if we flip NUM_BAD_HSDIRS
# times a coin that is biased with probability PREFIX_MATCH_PROB
# We want to learn the probability of accidentally camping at least two descriptors.
# So we want to know P(X >= 2):
#         P(X>=2) = 1 - P(X<2) = 1 - P(X<=1) = 1 - cdf(1)
# or for arbitrary P(X >= k) = 1 - cdf(k-1)

print "Results for scenario with binomial(n=%d, p=%s):" % (NUM_BAD_HSDIRS, '{:.22f}'.format(PREFIX_MATCH_PROB))
print "=" * 80

for k in xrange(7):
    print "Probability of %d HSDirs camping %d descriptor-ids of a hidden service" % (NUM_BAD_HSDIRS, k)
    if k == 0:
        prob = rv.pmf(0)
    else:
        prob = 1 - rv.cdf(k-1)
    print "\tP(X>=%d) = %s (aka %s)" % (k, (str(prob)), '{:.30f}'.format(prob))


