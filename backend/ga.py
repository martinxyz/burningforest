#!/usr/bin/env python3

import render
import random
import numpy as np
# import numpy.random
import matplotlib.pyplot as plt
import math
import dirichlet  # https://github.com/ericsuh/dirichlet

symbols = 'SJKLA+-[]\t'  # \t for end-of-sequence

def sample_system(pvals):
    def sample_rule(pvals):
        symlist = np.random.choice(list(symbols), 80, p=pvals)
        rule = ''.join(symlist).split('\t')[0]
        return rule

    system = {
        'w': 67,
        'h': 126,
        'axiom': 'S',
        'lineLength': 1.0 * random.random(),
        # 'angle': 1 + 180 * random.random(),
        'angle': 45,
        # 'iterations': math.ceil(random.random() * 5),
        'iterations': 8,
        'rules': {
          'S': sample_rule(pvals),
          'J': sample_rule(pvals),
          'K': sample_rule(pvals),
          'L': sample_rule(pvals),
          'A': sample_rule(pvals)
        }
    }
    return system


def evaluate_system(system):
    buf = render.render(system)
    loss = -buf.mean()
    return loss, buf


def evaluate_pvals(system):
    best_loss = None
    best_buf = None
    for i in range(20):
        system = sample_system(pvals)
        loss, buf = evaluate_system(system)
        if best_loss is None or loss < best_loss:
            best_loss = loss
            best_buf = buf
    return best_loss, best_buf


if __name__ == '__main__':
    iterations = 200

    best_factor = 0.02
    evaluations = 1000

    symbol_a = np.ones(len(symbols))
    # sentinel_a = np.ones(10)
    # create slight bias towards equal probability of all symbols
    symbol_a *= 2

    for it in range(iterations):
        print('iteration', it)
        sample = []
        loss_best = None
        res_best = None
        for i in range(evaluations):
            pvals = np.random.dirichlet(symbol_a)
            # pvals_sentinel = np.random.dirichlet(sentinel_a)
            loss, buf = evaluate_pvals(pvals)
            sample.append((loss, pvals, buf))

        sample.sort(key=lambda s: s[0])
        sample_loss = np.array([s[0] for s in sample])
        sample_pvals = np.array([s[1] for s in sample])
        sample_buf = np.array([s[2] for s in sample])

        res_best = sample_buf[1]

        print('mean loss was', sample_loss.mean())
        print('min loss was', sample_loss.min())
        plt.ion()
        plt.figure(1)
        plt.clf()
        plt.plot(sample_loss)
        plt.draw()
        # plt.show()
        plt.pause(0.1)

        # estimate new dirichlet distribution
        new_symbol_a = dirichlet.mle(sample_pvals[:int(evaluations*best_factor), :])
        print('old symbol_a:', symbol_a)
        print('new symbol_a:', new_symbol_a)
        # symbol_a = 0.5 * symbol_a + 0.5 * new_symbol_a
        symbol_a = new_symbol_a

        plt.figure(2)
        plt.clf()
        plt.imshow(res_best)
        plt.gray()
        plt.draw()
        plt.pause(0.1)
