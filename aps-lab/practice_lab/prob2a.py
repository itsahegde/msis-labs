import numpy as np
from math import comb
import matplotlib.pyplot as plt

np.random.seed(67)

n = 12
p = 0.20
minutes = 20000

failed_counts = []

for i in range(minutes):
    failures = 0
    for request in range(n):
        if np.random.rand() < p:
            failures += 1
    failed_counts.append(failures)

k_values = list(range(n+1))
emp_pmf = []

for k in k_values:
    count = 0
    for failure in failed_counts:
        if failure == k:
            count+=1
    prob = count/minutes
    emp_pmf.append(prob)

theo_pmf = []

for k in k_values:

    prob = (
        comb(n, k)
        * (p**k)
        * ((1-p)**(n-k))
    )

    theo_pmf.append(prob)

print("Number of failures | Empirical | Theoretical")
print("---------------------------------------------")

for i in range(len(k_values)):
    print(
        k_values[i], "                ",
        round(emp_pmf[i], 5), "   ",
        round(theo_pmf[i], 5)
    )

total_failures = 0
for failures in failed_counts:
    total_failures += failures
emp_mean = total_failures / minutes

theo_mean = n*p

print("\nExpectation")
print("Empirical:", round(emp_mean, 4))
print("Theoretical:", round(theo_mean, 4))

sq_diff = 0

for failure in failed_counts:
    diff = failure - emp_mean
    sq_diff += diff**2

emp_var = sq_diff / minutes

theo_var = n*p*(1-p)

print("\nVariance")
print("Empirical:", round(emp_var, 4))
print("Theoretical:", round(theo_var, 4))

count_atleast_4 = 0
for failures in failed_counts:
    if failures >= 4:
        count_atleast_4 += 1

emp_tail = count_atleast_4 / minutes
print("\nTail Probability")
print("Empirical:", round(emp_tail, 4))