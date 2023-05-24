import numpy as np
from cells import Cell
from tqdm import tqdm


class Simulation:
    def __init__(self, dt, Delta, D_sd, tau, t_sd, fila=0):
        self.dt = dt
        self.Delta_m = (Delta, D_sd)
        self.tau_m = (tau, t_sd)
        # self.Delta = 0.5 * (self.Delta_m[0] + np.random.normal(self.Delta_m[0], self.Delta_m[1]))
        # self.tau = 0.5 * (self.tau_m[0] + np.random.normal(self.tau_m[0], self.tau_m[1]))
        self.Delta = 0.5 * (self.Delta_m[0] - self.Delta_m[0]) + np.random.normal(0, self.Delta_m[1]) + self.Delta_m[0]
        self.tau = 0.5 * (self.tau_m[0] - self.tau_m[0]) + np.random.normal(0, self.tau_m[1]) + self.tau_m[0]

        self.all_cells = []

        self.fila = fila

    def run(self, length, vm, n=5):
        mother_cell = Cell(vm, self.Delta, self.tau, None, 0, self.fila)
        self.all_cells = [mother_cell]
        OD = [1]
        for i in tqdm(np.arange(0, length, self.dt)):
            count = 0
            for cell in self.all_cells:
                if not cell.divided:
                    count += 1
                    divide = cell.update_cell(self.dt, i)
                    if n is not None:
                        if divide and count <= n:   # assume n cells can survive in each iteration to reduce computation
                            # delta1 = 0.5 * (divide.Delta + np.random.normal(self.Delta_m[0], self.Delta_m[1]))
                            # delta2 = 0.5 * (divide.Delta + np.random.normal(self.Delta_m[0], self.Delta_m[1]))
                            # tau1 = 0.5 * (divide.tau + np.random.normal(self.tau_m[0], self.tau_m[1]))
                            # tau2 = 0.5 * (divide.tau + np.random.normal(self.tau_m[0], self.tau_m[1]))
                            delta1 = 0.5 * (divide.Delta - self.Delta_m[0]) + np.random.normal(0, self.Delta_m[1]) \
                                     + self.Delta_m[0]
                            delta2 = 0.5 * (divide.Delta - self.Delta_m[0]) + np.random.normal(0, self.Delta_m[1]) \
                                     + self.Delta_m[0]
                            tau1 = 0.5 * (divide.tau - self.tau_m[0]) + np.random.normal(0, self.tau_m[1]) \
                                   + self.tau_m[0]
                            tau2 = 0.5 * (divide.tau - self.tau_m[0]) + np.random.normal(0, self.tau_m[1]) \
                                   + self.tau_m[0]
                            # add noise in division volume
                            daughter1 = Cell(divide.v[-1]/2, delta1, tau1, divide, i, self.fila)
                            daughter2 = Cell(divide.v[-1]/2, delta2, tau2, divide, i, self.fila)
                            divide.daughters = (daughter1, daughter2)
                            divide.td = i
                            self.all_cells.append(daughter1)
                            self.all_cells.append(daughter2)
                    else:
                        if divide:
                            # delta1 = 0.5 * (divide.Delta + np.random.normal(self.Delta_m[0], self.Delta_m[1]))
                            # delta2 = 0.5 * (divide.Delta + np.random.normal(self.Delta_m[0], self.Delta_m[1]))
                            # tau1 = 0.5 * (divide.tau + np.random.normal(self.tau_m[0], self.tau_m[1]))
                            # tau2 = 0.5 * (divide.tau + np.random.normal(self.tau_m[0], self.tau_m[1]))
                            delta1 = 0.5 * (divide.Delta - self.Delta_m[0]) + np.random.normal(0, self.Delta_m[1]) \
                                     + self.Delta_m[0]
                            delta2 = 0.5 * (divide.Delta - self.Delta_m[0]) + np.random.normal(0, self.Delta_m[1]) \
                                     + self.Delta_m[0]
                            tau1 = 0.5 * (divide.tau - self.tau_m[0]) + np.random.normal(0, self.tau_m[1]) \
                                   + self.tau_m[0]
                            tau2 = 0.5 * (divide.tau - self.tau_m[0]) + np.random.normal(0, self.tau_m[1]) \
                                   + self.tau_m[0]
                            daughter1 = Cell(divide.v[-1] / 2, delta1, tau1, divide, i, self.fila)
                            daughter2 = Cell(divide.v[-1] / 2, delta2, tau2, divide, i, self.fila)
                            divide.daughters = (daughter1, daughter2)
                            divide.td = i
                            self.all_cells.append(daughter1)
                            self.all_cells.append(daughter2)
            OD.append(count)
        return OD
