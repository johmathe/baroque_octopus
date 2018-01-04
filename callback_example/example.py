import my_lib
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt

plt.figure()
x = np.arange(0.0, 5.0, 0.1)
my_lib.solve(x, plt.plot)
plt.savefig('result.png')
