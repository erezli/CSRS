import numpy as np


class Cell:
    def __init__(self, vb, Delta, tau, parent, tb):
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

    def growth_rate(self, dt):
        return 2 ** (dt/self.tau)   # add uncertainty

    def update_cell(self, dt, t):
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
