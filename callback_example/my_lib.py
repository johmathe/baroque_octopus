import numpy as np

N_ITER = 5

def solve(plot_callback=None):
    x = np.arange(0.0, 5.0, 0.1)
    for i in range(N_ITER):
        y = np.sin(i*x)
        if plot_callback is not None:
            plot_callback(y)
