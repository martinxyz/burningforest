#!/usr/bin/env python3

import render
import random
import numpy
import numpy.random
import scipy.misc
import math

symbols = 'SJKLA+-[]\t'  # \t for end-of-sequence

symbol_a = numpy.ones(len(symbols))
# create slight bias towards equal probability of all symbols
symbol_a *= 2

pvals = numpy.random.dirichlet(symbol_a)


def sample_system(pvals):
    def sample_rule(pvals):
        symlist = numpy.random.choice(list(symbols), 80, p=pvals)
        rule = ''.join(symlist).split('\t')[0]
        return rule

    system = {
        'w': 67,
        'h': 126,
        'axiom': 'S',
        'lineLength': 20 * random.random(),
        'angle': 1 + 180 * random.random(),
        'iterations': math.ceil(random.random() * 5),
        'rules': {
          'S': sample_rule(pvals),
          'J': sample_rule(pvals),
          'K': sample_rule(pvals),
          'L': sample_rule(pvals),
          'A': sample_rule(pvals)
        }
    }
    return system


for i in range(80):
    system = sample_system(pvals)
    buf = render.render(system)
    scipy.misc.imsave('ga-test-%04d.png' % i, buf)
