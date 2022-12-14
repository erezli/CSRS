import numpy as np
from cells import Cell
from tqdm import tqdm


class Simulation:
    def __init__(self, dt, Delta, D_sd, tau, t_sd):
        self.dt = dt
        self.Delta_m = (Delta, D_sd)
        self.tau_m = (tau, t_sd)
        self.Delta = 0.5 * (self.Delta_m[0] + np.random.normal(self.Delta_m[0], self.Delta_m[1]))
        self.tau = 0.5 * (self.tau_m[0] + np.random.normal(self.tau_m[0], self.tau_m[1]))

        self.all_cells = []

    def run(self, length, vm):
        mother_cell = Cell(vm, self.Delta, self.tau, None, 0)
        self.all_cells = [mother_cell]
        for i in tqdm(np.arange(0, length, self.dt)):
            count = 0
            for cell in self.all_cells:
                if not cell.divided:
                    count += 1
                    divide = cell.update_cell(self.dt, i)
                    if divide and count <= 5:   # assume five cells can survive in each iteration to reduce computation
                        delta1 = 0.5 * (divide.Delta + np.random.normal(self.Delta_m[0], self.Delta_m[1]))
                        delta2 = 0.5 * (divide.Delta + np.random.normal(self.Delta_m[0], self.Delta_m[1]))
                        tau1 = 0.5 * (divide.tau + np.random.normal(self.tau_m[0], self.tau_m[1]))
                        tau2 = 0.5 * (divide.tau + np.random.normal(self.tau_m[0], self.tau_m[1]))
                        daughter1 = Cell(divide.v[-1]/2, delta1, tau1, divide, i)
                        daughter2 = Cell(divide.v[-1]/2, delta2, tau2, divide, i)
                        divide.daughters = (daughter1, daughter2)
                        divide.td = i
                        self.all_cells.append(daughter1)
                        self.all_cells.append(daughter2)
