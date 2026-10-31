import numpy as np

np.random.seed(67)

n = 10000
p_fraud = 0.08
p_detect = 0.85
p_falsealarm = 0.10

true_status = []
flag_status = []

for i in range(n):

    if np.random.rand() < p_fraud:
        fraud = True
    else:
        fraud = False

    if fraud == True:
        if np.random.rand() < p_detect:
            flagged = True
        else:
            flagged = False

    else:
        if np.random.rand() < p_falsealarm:
            flagged = True
        else:
            flagged = False

    true_status.append(fraud)
    flag_status.append(flagged)

TP, FN, FP, TN = 0, 0, 0, 0

for i in range(n):
    if true_status[i]==True and flag_status[i]==True:
        TP += 1
    elif true_status[i]==True and flag_status[i]==False:
        FN+=1
    elif true_status[i]==False and flag_status[i]==True:
        FP+=1
    else:
        TN+=1

print("Confusion matrix: ")
print("                 Flagged    Not Flagged")
print("Fraudulent       ", TP, "       ", FN)
print("Genuine          ", FP, "       ", TN)

p_flag_sim = (TP + FP) / n
p_flag_given_fraud_sim = TP/(TP+FN)
p_fraud_given_flag_sim = TP/(TP+FP)

p_genuine = 1 - p_fraud

p_flag_theory = (
    p_detect*p_fraud + p_falsealarm*p_genuine
)

p_fraud_given_flag_theory = (
    p_detect*p_fraud / p_flag_theory
)

print("\nProbability Comparison")
print("----------------------")

print("P(flag)")
print("Simulated:", round(p_flag_sim, 4))
print("Theoretical:", round(p_flag_theory, 4))

print("\nP(flag | fraud)")
print("Simulated:", round(p_flag_given_fraud_sim, 4))
print("Theoretical:", p_detect)

print("\nP(fraud | flag)")
print("Simulated:", round(p_fraud_given_flag_sim, 4))
print("Theoretical:", round(p_fraud_given_flag_theory, 4))
