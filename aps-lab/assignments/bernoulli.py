import numpy as np

p = 0.3
sample_size = 20

np.random.seed(42)
samples = np.random.binomial(n=1, p=p, size = sample_size)

print(samples)

print(f"Number of samples of 0: {np.sum(samples==0)}")
print(f"Number of samples of 1: {np.sum(samples==1)}")

print(f"Percentage of samples of 0: {np.sum(samples==0)*100/sample_size}")
print(f"Percentage of samples of 1: {np.sum(samples==1)*100/sample_size}")

import matplotlib.pyplot as plt

x = np.array([0, 1])

y = np.array([np.sum(samples==0), np.sum(samples==1)])

plt.bar(x, y)
plt.xticks(np.array([0, 1]))
plt.show()

exp = np.sum(x)