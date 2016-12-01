import numpy as np

from article_to_vec import CATEGORIES

def recall(predicted, actual):
    n = len(CATEGORIES)

    c_mat = np.zeros((n, n))

    for i in range(predicted.shape[0]):
        c_mat[int(actual[i][0])][int(predicted[i][0])] += 1


    recall_mat = np.sum(c_mat, axis=1)
    for i, _ in enumerate(CATEGORIES):
        if recall_mat[i] == 0:
            recall_mat[i] = 0
        else:
            recall_mat[i] = c_mat[i][i] / recall_mat[i]

    acc_mat = np.sum(c_mat, axis=0)
    for i, _ in enumerate(CATEGORIES):
        if acc_mat[i] == 0:
            acc_mat[i] = 0
        else:
            acc_mat[i] = c_mat[i][i] / acc_mat[i]

    print(" " * 8, end="")
    for i, cat in enumerate(CATEGORIES):
        print("%-8s" % cat, end="")
    print()
    for i, cat in enumerate(CATEGORIES):
        print("%-8s" % cat, end="")
        for j in c_mat[i]:
            print("%-8d" % int(j), end="")
        print("acc: %-8f recall %-8f" % (acc_mat[i]*100, recall_mat[i]*100))

    print("Max Acc: %f %% " % (np.max(acc_mat) * 100, ))
    print("Max Recall: %f %% " % (np.max(recall_mat) * 100, ))
    print("Min Acc: %f %% " % (np.min(acc_mat) * 100, ))
    print("Min Recall: %f %% " % (np.min(recall_mat) * 100, ))
    print("Mean Acc: %f %% " % (np.mean(acc_mat) * 100, ))
    print("Mean Recall: %f %% " % (np.mean(recall_mat) * 100, ))
