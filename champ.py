#! python2
# coding:utf-8

import numpy as np
import matplotlib.pyplot as plt

total = 30
Rows = 5
Cols = 6

x = np.linspace(0, 3, 100)
for i in range(total):
    plt.subplot(Rows, Cols, i + 1)
    plt.plot(x, np.sin(x * ((i + 1) % Rows + 1)))

plt.show()