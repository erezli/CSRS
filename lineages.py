from simulation import Simulation
import numpy as np
import matplotlib.pyplot as plt
import scipy


class Lineage:
    def __init__(self, simulations, cell=-1):
        self.lineages = []
        self.times = []
        self.divisions_idx = []
        self.divisions_t = []
        for simulation in simulations:
            # pick a lineage
            last_cell = simulation.all_cells[cell]
            lineage = np.array([])
            time = np.array([])
            i_div = []
            t_div = []
            while last_cell:
                lineage = np.concatenate((np.array(last_cell.v), lineage))
                time = np.concatenate((np.array(last_cell.t), time))
                if last_cell.parent:
                    i_div.insert(0, round(last_cell.tb / simulation.dt))
                    t_div.insert(0, last_cell.tb)
                last_cell = last_cell.parent
            self.lineages.append(lineage)
            self.times.append(time)
            self.divisions_idx.append(i_div)
            self.divisions_t.append(t_div)

    def plot(self):
        for t, l, d, x in zip(self.times, self.lineages, self.divisions_t, self.divisions_idx):
            plt.plot(t, l)
            plt.vlines(d, 0, np.array(l)[x], '0.5', 'dashed')
        plt.show()

    def downsample(self, n=2, plot=True):
        samples = [ln[::n] for ln in self.lineages]
        times = [t[::n] for t in self.times]
        if plot:
            for t, l, L, d, x in zip(times, samples, self.lineages, self.divisions_t, self.divisions_idx):
                plt.plot(t, l)
                plt.vlines(d, 0, np.array(L)[x], '0.5', 'dashed')
            plt.show()
        return samples, times

    def find_division(self, samples, times, i, height=None, threshold=None, distance=None, plot=True):
        idx, _ = scipy.signal.find_peaks(samples[i], height=height, threshold=threshold, distance=distance)
        if plot:
            plt.plot(times[i], samples[i])
            plt.plot(times[i][idx], samples[i][idx], "x", label="measured division")
            plt.plot(self.divisions_t[i], self.lineages[i][np.array(self.divisions_idx[i])], "o", label="true division")
            plt.legend()
            plt.show()
        return idx

    def collect_downsampled_data(self, n=2):
        samples, times = self.downsample(n, plot=False)
        div_ts = []
        div_ls = []
        for i in range(len(samples)):
            idx = self.find_division(samples, times, i, plot=False)
            div_times = [times[i][idx[j+1]] - times[i][idx[j]] for j in range(len(idx) - 1)]
            div_ts.append(div_times)
            div_lengths = [samples[i][j] for j in idx]
            div_ls.append(div_lengths)
        return div_ts, div_ls

