#!/usr/bin/env python3

import render
import numpy as np
import matplotlib.pyplot as plt
import scipy.misc
import dask
import dask.multiprocessing
import repr

symbols = 'SJKLA+-[]\t'  # \t for end-of-sequence


def sample_system(ind):
    def sample_rule(pvals):
        symlist = np.random.choice(list(symbols), 80, p=pvals)
        rule = ''.join(symlist).split('\t')[0]
        return rule

    system = {
        'w': 67,
        'h': 126,
        'axiom': 'S',
        # 'lineLength': 1.0 * random.random(),
        'lineLength': ind['lineLength'] * 12,
        'lineWidth': ind['lineWidth'] * 12,
        # 'angle': 1 + 180 * random.random(),
        'angle': ind['angle'] * 50,
        # 'iterations': math.ceil(random.random() * 5),
        'iterations': 3,
        'rules': {
          'S': sample_rule(ind['pvals']),
          'J': sample_rule(ind['pvals']),
          'K': sample_rule(ind['pvals']),
          'L': sample_rule(ind['pvals']),
          'A': sample_rule(ind['pvals'])
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


def evaluate_ind(ind):
    best_loss = None
    best_buf = None
    for i in range(20):
        system = sample_system(ind)
        loss, buf = evaluate_system(system)
        if best_loss is None or loss < best_loss:
            best_loss = loss
            best_buf = buf
    return (best_loss, ind, best_buf)


def main():
    iterations = 150

    best_factor = 0.02
    evaluations = 5000

    population = repr.Population({
        'pvals': repr.DirichletParam(len(symbols)),
        'lineWidth': repr.BetaParam(),
        'lineLength': repr.BetaParam(),
        'angle': repr.BetaParam(),
    })

    for it in range(iterations):
        print('iteration', it)
        sample = []
        for i in range(evaluations):
            ind = population.sample()
            res = dask.delayed(evaluate_ind)(ind)
            sample.append(res)

        sample = dask.compute(*sample, get=dask.multiprocessing.get)
        sample = list(sample)

        sample.sort(key=lambda s: s[0])
        sample_loss = np.array([s[0] for s in sample])
        sample_inds = np.array([s[1] for s in sample])
        sample_buf = np.array([s[2] for s in sample])

        res_best = sample_buf[0]

        print(50 * '-')
        print('best ind:', sample_inds[0])
        print('min loss was', sample_loss.min())
        print('mean loss was', sample_loss.mean())
        plt.ion()
        plt.figure(1)
        plt.clf()
        plt.plot(sample_loss)
        plt.draw()
        # plt.show()
        plt.pause(0.1)

        # estimate new distribution
        top_inds = sample_inds[:int(evaluations*best_factor)]
        population.update(top_inds)
        print('population:', population)

        plt.figure(2)
        plt.clf()
        plt.imshow(res_best)
        plt.gray()
        plt.draw()
        plt.pause(0.1)

if __name__ == '__main__':
    main()
