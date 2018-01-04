import numpy as np

def solve(x, plot_callback):
    y = np.sin(x)
    plot_callback(x, y)
