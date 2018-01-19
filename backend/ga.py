#!/usr/bin/env python3

import render
import numpy as np
import matplotlib.pyplot as plt
import scipy.misc
import math
import random
import sys
import os
import json
import pprint
import dask
import dask.delayed
import dask.multiprocessing
import time
import repr


symbols = 'SJKA+-[]<>\t'  # \t for end-of-sequence


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


if len(sys.argv) > 1:
    outdir = sys.argv[1]
else:
    outdir = './output'
os.makedirs(outdir)


def sample_system(ind):
    def sample_rule(pvals):
        symlist = np.random.choice(list(symbols), 80, p=pvals)
        rule = ''.join(symlist).split('\t')[0]
        return rule

    def logrange(p, min, max):
        return min * math.exp(p * math.log(max/min))

    system = {
        'w': 67*4,
        'h': 126*4,
        'axiom': sample_rule(ind['axiom']),
        # 'lineLength': logrange(ind['lineLength'], 1, 40),
        # 'lineWidth': logrange(ind['lineWidth'], 1, 40),
        'limit': 5000,
        'lineLength': 5*4,
        'lineWidth': 3*4,
        'scaleStep': 1.0 + logrange(ind['scaleStep'], 0.001, 0.5),
        'angle': logrange(ind['angle'], 5, 200),
        'angle0': ind['angle0'] * 180,
        'iterations': math.floor(ind['iterations'] * 5),
        'rules': {
          'S': sample_rule(ind['S']),
          'J': sample_rule(ind['J']),
          'K': sample_rule(ind['K']),
          # 'L': sample_rule(ind['L']),
          # 'A': sample_rule(ind['A'])
        }
    }

    # if not ind['S-enable']: system['rules']['S'] = 'S'
    # if not ind['J-enable']: system['rules']['J'] = 'J'
    # if not ind['K-enable']: system['rules']['K'] = 'K'
    # if not ind['L-enable']: system['rules']['L'] = 'L'
    # if not ind['A-enable']: system['rules']['A'] = 'A'

    # system = {
    #     'w': 67,
    #     'h': 126,
    #     'angle': ind['angle'] * 180,
    #     'iterations': 3,
    #     'lineLength': ind['lineLength'] * 12,
    #     'lineWidth': ind['lineWidth'] * 12,
    #     'axiom': 'GGGGGG',
    #     'rules': {
    #         'G': 'G++[F]',
    #         'F': '-----F---[G]'
    #     }
    # }
    return system


value_img = scipy.misc.imread('./template1.png')[:,:,0]
def evaluate_system(system):
    try:
        buf = render.render(system)
    except ValueError:
        return 999, None

    # loss = -(buf.astype('float') * (value_img.astype('float') - 127))
    # loss[loss > 0] *= 4
    # loss = loss.mean()
    # if loss < -100:
    if False:
        plt.figure(5)
        plt.clf()
        plt.imshow(buf.astype('float') * (value_img.astype('float') - 127))
        plt.colorbar()
        plt.draw()
        plt.pause(2.5)

    buf2 = buf.astype('float') / 256
    loss = 0
    loss -= np.abs(np.diff(buf2.flatten())).mean()
    loss -= np.abs(np.diff(buf2.transpose().flatten())).mean()
    loss += 200*(buf2.mean()-0.3)**2
    return loss, buf


def evaluate_ind(ind):
    best_loss = None
    best_buf = None
    for i in range(200):
        system = sample_system(ind)
        loss, buf = evaluate_system(system)
        if best_loss is None or loss < best_loss:
            best_loss = loss
            best_buf = buf
    return (best_loss, ind, best_buf)


def main():
    iterations = 15000

    best_factor = 0.01
    evaluations = 5000

    population = repr.Population({
        'axiom': repr.DirichletParam(len(symbols)),
        'S': repr.DirichletParam(len(symbols)),
        'J': repr.DirichletParam(len(symbols)),
        'K': repr.DirichletParam(len(symbols)),
        # 'L': repr.DirichletParam(len(symbols)),
        # 'A': repr.DirichletParam(len(symbols)),
        'iterations': repr.BetaParam(),
        'lineWidth': repr.BetaParam(),
        'scaleStep': repr.BetaParam(),
        'lineLength': repr.BetaParam(),
        'angle': repr.BetaParam(),
        'angle0': repr.BetaParam(),
        # 'S-enable': repr.BernoulliParam(),
        # 'J-enable': repr.BernoulliParam(),
        # 'K-enable': repr.BernoulliParam(),
        # 'L-enable': repr.BernoulliParam(),
        # 'A-enable': repr.BernoulliParam(),
        'no-op1': repr.DirichletParam(len(symbols)),
        'no-op2': repr.DirichletParam(len(symbols)),
        'no-op3': repr.BetaParam(),
        'no-op4': repr.BetaParam(),
        # 'no-op5': repr.BernoulliParam(),
        # 'no-op6': repr.BernoulliParam(),
    })

    for it in range(iterations):
        with open(outdir + '/current.txt', 'w') as f:
            f.write('iteration %d' % it)
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
        print(sample_buf[0].shape)

        for kk in range(10):
            fn = outdir + f'/it{it:04}-best{kk:03}'
            scipy.misc.imsave(fn + '.png', sample_buf[kk])
            with open(fn + '-ind.json', 'w') as f:
                f.write(json.dumps(sample_inds[kk], indent=4, cls=NumpyEncoder))

        for kk in range(10):
            kkk = random.randrange(len(sample_buf))
            fn = outdir + f'/it{it:04}-random{kk:03}'
            if sample_buf[kkk] is not None:
                scipy.misc.imsave(fn + '.png', sample_buf[kkk])
            with open(fn + '-ind.json', 'w') as f:
                f.write(json.dumps(sample_inds[kkk], indent=4, cls=NumpyEncoder))

        print(50 * '-')
        print('best ind:')
        pprint.pprint(sample_inds[0])
        print('min loss   :', sample_loss.min())
        print('median loss:', np.median(sample_loss))
        print('mean loss  :', sample_loss.mean())
        # plt.ion()
        # plt.figure(1)
        # plt.clf()
        # plt.plot(sample_loss)
        # plt.draw()
        # # plt.show()
        # plt.pause(0.1)

        # estimate new distribution
        top_inds = sample_inds[:int(evaluations*best_factor)]
        population.update(top_inds)
        print('population:', population)

        with open(outdir + f'/it{it:04}-info.json', 'w') as f:
            d = dict(
                iteration = it,
                min_loss = sample_loss.min(),
                mean_loss = sample_loss.mean(),
                median_loss = np.median(sample_loss),
                timestamp = time.time(),
                )
            f.write(json.dumps(d, indent=4))
        with open(outdir + f'/it{it:04}-info.txt', 'w') as f:
            print('population:', population, file=f)

if __name__ == '__main__':
    main()
