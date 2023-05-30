import numpy as np
import random
from scipy.stats import expon
from scipy.stats import poisson


class Cell:
    def __init__(self, vb, Delta, tau, parent, tb, fila=0):
        self.vb = vb
        self.Delta = Delta
        self.tau = tau
        self.parent = parent
        self.tb = tb

        self.daughters = (None, None)
        self.divided = False
        self.td = None
        self.v = [self.vb]
        self.t = [self.tb]

        self.filamentation = random.choices([True, False], weights=[fila, 1 - fila])[0]
        if self.filamentation:
            # self.fila_Delta = random.uniform(1.001, 5.5) * Delta
            # self.fila_Delta = 0.5 * (poisson.rvs(0.02, 2, 1)) * Delta
            # self.fila_Delta = (poisson.rvs(0.02, 1, 1)) * Delta
            self.fila_Delta = (expon.rvs(1, 0.25, 1)) * Delta
            offest_p = 0.002
            if random.choices([True, False], weights=[offest_p, 1 - offest_p])[0]:
                # very long cell
                self.fila_Delta = random.uniform(1, 8) * Delta

    def growth_rate(self, dt):
        return 2 ** (dt/self.tau)   # add uncertainty

    def update_cell(self, dt, t):
        if self.filamentation:
            if self.v[-1] - self.vb < self.fila_Delta:
                self.v.append(self.v[-1] * (self.growth_rate(dt)))
                self.t.append(t)
                return False
            else:
                self.v = np.array(self.v)
                self.t = np.array(self.t)
                self.divided = True
                return self
        else:
            if self.v[-1] - self.vb < self.Delta:
                self.v.append(self.v[-1]*(self.growth_rate(dt)))
                self.t.append(t)
                return False
            else:
                self.v = np.array(self.v)
                self.t = np.array(self.t)
                self.divided = True
                return self

    def assign_daughter(self, daughters):
        self.daughters = (daughters[0], daughters[1])
