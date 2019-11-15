import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# matrix A
A = np.loadtxt('array.txt', dtype=np.float64)


#  this function creates a plot of the Sterilization time, lasting 30 minutes
# step in seconds
def create_active_plot(step: int) -> None:
    global A
    a = A.T[::step].T
    # matrix containing random coefficients
    coefs = np.random.dirichlet(np.ones(a.shape[0]), size=1)[0]
    # apply dot product of coefs with each column of A
    result = np.array([np.dot(a[:, i], coefs) for i in range(a.shape[1])])
    pd.DataFrame(result).plot()
    plt.show()


step = ''
while step != 'exit':
    step = input('Enter your step in seconds:')
    create_active_plot(int(step))
