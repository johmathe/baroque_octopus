import numpy as np

def solve(x, plot_callback=None):
    y = np.sin(x)
    if plot_callback is not None:
        plot_callback(x, y)
