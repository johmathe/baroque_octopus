import my_lib
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt

class Viz:
    def __init__(self):
        self.debug_values = []

    def callback(self, param):
        self.debug_values.append(param)

    def plot(self):
        plt.figure()
        for data in self.debug_values:
            plt.plot(data)
        plt.savefig('result.png')


if __name__ == '__main__':
    viz = Viz()
    my_lib.solve(viz.callback)
    viz.plot()
