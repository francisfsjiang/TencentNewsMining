import numpy as np
import sklearn.svm
import h5py

from evaluate import recall

if __name__ == "__main__":
    print("sklearn svm calculating")

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
    train_cat_mat = train_cat_mat.reshape(train_cat_mat.shape[0])
    train_id_mat = id_mat[mask]

    mask = np.ones(art_mat.shape[0], np.bool)
    mask[choice] = 0
    test_art_mat = art_mat[mask]
    test_cat_mat = cat_mat[mask]
    test_cat_mat = test_cat_mat.reshape(test_cat_mat.shape[0])
    test_id_mat = id_mat[mask]

    clf = sklearn.svm.SVC(
        decision_function_shape='ovr',
        cache_size=1000,
    )
    clf.fit(train_art_mat, train_cat_mat)

    result = clf.predict(train_art_mat)
    acc = np.sum(result == train_cat_mat) / result.shape[0]
    print("ACC on train set: %f%% " % (acc * 100))

    result = clf.predict(test_art_mat)
    acc = np.sum(result == test_cat_mat) / result.shape[0]
    print("ACC: %f%% " % (acc * 100))

    recall(result, test_cat_mat)
