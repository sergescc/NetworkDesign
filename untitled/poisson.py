from  scipy.stats import poisson
import matplotlib.pyplot as plt
import numpy as np

dist = poisson(20)
variables = dist.rvs(1000)
bins = np.arange(0,50)

plt.hist(variables, bins,  normed=True, alpha=.3,color='green')
plt.xticks(np.arange(0,50,5))
plt.title("PMF lambda=20 N=1000")
plt.xlabel("Arrival Counts")
plt.ylabel("Probability")
plt.show()