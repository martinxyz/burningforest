import random
import dirichlet  # https://github.com/ericsuh/dirichlet
import numpy as np


class BernoulliParam:
    def __init__(self):
        self.p = 0.5

    def sample(self):
        if random.random() < self.p:
            return 0
        else:
            return 1

    def update(self, samples):
        mle = np.mean(samples)
        self.p = 0.5 * self.p + 0.5 * mle

    def __repr__(self):
        return 'Param(p=%r)' % self.p


class DirichletParam:
    def __init__(self, N):
        self.alpha = np.ones(N)

    def sample(self):
        return np.random.dirichlet(self.alpha)

    def update(self, samples):
        try:
            mle = dirichlet.mle(np.array(samples))
        except Exception as err:
            print('DIRICHLET EXCEPTION', err)
            mle = self.alpha

        # avoid the above exception in the first place
        if mle.sum() > 1000:
            mle *= 1000 / mle.sum()
        mle = mle.clip(0.1, None)

        self.alpha = 0.5 * self.alpha + 0.5 * mle

    def __repr__(self):
        return 'Param(alpha=%r)' % self.alpha


class BetaParam(DirichletParam):
    def __init__(self):
        super().__init__(2)

    def sample(self):
        return super().sample()[0]

    def update(self, samples):
        samples = [(p, 1-p) for p in samples]
        super().update(samples)


class Population:
    def __init__(self, params):
        self.params = params

    def sample(self):
        ind = {}
        for name, param in self.params.items():
            ind[name] = param.sample()
        return ind

    def update(self, samples):
        for name, param in self.params.items():
            param.update([ind[name] for ind in samples])

    def __repr__(self):
        return 'Population[\n%r\n]\n' % self.params
