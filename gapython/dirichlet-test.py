import numpy as np
import dirichlet  # https://github.com/ericsuh/dirichlet

symbols = 'SJKLA+-[]\t'  # \t for end-of-sequence
symbol_a = np.ones(len(symbols))

evaluations = 20
iterations = 20000
for it in range(iterations):
    sample_pvals = []
    for i in range(evaluations):
        tmp = np.random.dirichlet(symbol_a)
        # p = tmp[0] * 0.9
        # tmp[0] -= p
        # tmp[1] += p

        before = tmp.copy()
        tmp /= 10
        tmp[0] += (before - tmp).sum()
        sample_pvals.append(tmp)
    sample_pvals = np.array(sample_pvals)

    print('iteration', it)
    print('params:', symbol_a)
    print('probs:', np.random.dirichlet(symbol_a))

    # print(symbol_a.sum())
    symbol_a = dirichlet.mle(sample_pvals)
    if symbol_a.sum() > 1000:
        symbol_a *= 1000 / symbol_a.sum()
    symbol_a = symbol_a.clip(0.1, None)
