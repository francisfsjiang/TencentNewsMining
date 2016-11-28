import pickle
import h5py
import numpy as np

from ta_model import CATEGORIES


if __name__ == "__main__":
    print("Bayes calculating")

    file = h5py.File('article_mat.h5', 'r')
    art_mat = file['art_mat'][:]
    cat_mat = file['cat_mat'][:]
    id_mat  = file['id_mat' ][:]
    file.close()

    choice = np.random.choice(art_mat.shape[0], art_mat.shape[0] // 2, replace=False)
    mask = np.zeros(art_mat.shape[0], np.bool)
    mask[choice] = 1
    train_art_mat = art_mat[mask]
    train_cat_mat = cat_mat[mask]
    train_id_mat = id_mat[mask]

    mask = np.ones(art_mat.shape[0], np.bool)
    mask[choice] = 0
    test_art_mat = art_mat[mask]
    test_cat_mat = cat_mat[mask]
    test_id_mat = id_mat[mask]

    beyas_mat = np.zeros((len(CATEGORIES), train_art_mat.shape[1]))
    p_cat_mat = np.zeros((len(CATEGORIES),))
    for cat in range(len(CATEGORIES)):
        idx = np.where(train_cat_mat == cat)[0]
        p_cat_mat[cat] = idx.shape[0] / train_cat_mat.shape[0]
        cur_art_mat = train_art_mat[idx]

        beyas_mat[cat][:] = np.log(np.sum(cur_art_mat, axis=0) + 1 / cur_art_mat.shape[0])

    result = np.argmax(beyas_mat.dot(train_art_mat.T), axis=0)
    result = result.reshape(result.shape[0], 1)
    acc = np.sum(result == train_cat_mat) / result.shape[0]
    print("ACC on train set: %f%% " % (acc * 100))

    result = np.argmax(beyas_mat.dot(test_art_mat.T), axis=0)
    result = result.reshape(result.shape[0], 1)
    acc = np.sum(result == test_cat_mat) / result.shape[0]
    print("ACC: %f%% " % (acc * 100))
