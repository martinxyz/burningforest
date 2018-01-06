#!/usr/bin/env python3

import render
import random
import numpy as np
# import numpy.random
import matplotlib.pyplot as plt
import scipy.misc
import dask
import dask.multiprocessing
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
        # 'lineLength': 1.0 * random.random(),
        'lineLength': 4,
        'lineWidth': 8,
        # 'angle': 1 + 180 * random.random(),
        'angle': 20,
        # 'iterations': math.ceil(random.random() * 5),
        'iterations': 3,
        'rules': {
          'S': sample_rule(pvals),
          'J': sample_rule(pvals),
          'K': sample_rule(pvals),
          'L': sample_rule(pvals),
          'A': sample_rule(pvals)
        }
    }
    return system

value_img = scipy.misc.imread('./template1.png')[:,:,0]
def evaluate_system(system):
    buf = render.render(system)

    loss = -(buf.astype('float') * (value_img.astype('float') - 127)).mean()
    # if loss < -100:
    if False:
        plt.figure(5)
        plt.clf()
        plt.imshow(buf.astype('float') * (value_img.astype('float') - 127))
        plt.colorbar()
        plt.draw()
        plt.pause(2.5)

    # loss = -buf.mean()
    return loss, buf


def evaluate_pvals(pvals):
    best_loss = None
    best_buf = None
    for i in range(20):
        system = sample_system(pvals)
        loss, buf = evaluate_system(system)
        if best_loss is None or loss < best_loss:
            best_loss = loss
            best_buf = buf
    return (best_loss, pvals, best_buf)


def main():
    iterations = 150

    best_factor = 0.02
    evaluations = 5000

    symbol_a = np.ones(len(symbols))
    # sentinel_a = np.ones(10)
    # create slight bias towards equal probability of all symbols
    symbol_a *= 2

    for it in range(iterations):
        print('iteration', it)
        sample = []
        for i in range(evaluations):
            pvals = np.random.dirichlet(symbol_a)
            res = dask.delayed(evaluate_pvals)(pvals)
            sample.append(res)

        sample = dask.compute(*sample, get=dask.multiprocessing.get)
        sample = list(sample)

        sample.sort(key=lambda s: s[0])
        sample_loss = np.array([s[0] for s in sample])
        sample_pvals = np.array([s[1] for s in sample])
        sample_buf = np.array([s[2] for s in sample])

        res_best = sample_buf[0]

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
        print('new symbol_a:', new_symbol_a)
        # symbol_a = 0.5 * symbol_a + 0.5 * new_symbol_a
        symbol_a = new_symbol_a

        plt.figure(2)
        plt.clf()
        plt.imshow(res_best)
        plt.gray()
        plt.draw()
        plt.pause(0.1)

if __name__ == '__main__':
    main()
