import numpy as np

from ta_model import CATEGORIES


def recall(predicted, actual):
    n = len(CATEGORIES)

    c_mat = np.zeros((n, n))

    for i in range(predicted.shape[0]):
        c_mat[int(actual[i][0])][int(predicted[i][0])] += 1


    r_mat = np.sum(c_mat, axis=1)
    for i, _ in enumerate(CATEGORIES):
        r_mat[i] = c_mat[i][i] / r_mat[i]

    print("Recall: %f %% " % (np.mean(r_mat) * 100, ))

    print(" " * 8, end="")
    for i, cat in enumerate(CATEGORIES):
        print("%-8s" % cat, end="")
    print()
    for i, cat in enumerate(CATEGORIES):
        print("%-8s" % cat, end="")
        for j in c_mat[i]:
            print("%-8d" % int(j), end="")
        print()
