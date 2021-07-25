import numpy as np


def sliding_window(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def get_ranges(att, lbl, num_lbl=0):
    idx = np.argsort(att)
    att_sorted = att[idx]
    lbl_sorted = lbl[idx]

    a_dif = np.diff(att_sorted)
    lbl_dif = np.diff(lbl_sorted)

    splits = np.logical_or(a_dif == 0, lbl_dif == 0)
    result = np.where(splits == False)[0] + 1
    print(result)
    splt = np.split(att_sorted, result)
    ranges = np.array([[a[0], a[-1]] for a in splt])
    lbl_splt = np.split(lbl_sorted, result)
    counts = np.array([np.bincount(a, minlength=num_lbl) for a in lbl_splt])
    return counts, ranges


def get_data():
    # TODO: delete later, Used now while developing only
    v = np.array([5.1, 4.9, 4.7, 4.6, 5., 5.4, 4.6, 5., 4.4, 4.9, 5.4, 4.8, 4.8, 4.3, 5.8, 5.7, 5.4
                     , 5.1, 5.7, 5.1, 5.4, 5.1, 4.6, 5.1, 4.8, 5., 5., 5.2, 5.2, 4.7, 4.8, 5.4, 5.2, 5.5, 4.9
                     , 5., 5.5, 4.9, 4.4, 5.1, 5., 4.5, 4.4, 5., 5.1, 4.8, 5.1, 4.6, 5.3, 5., 7., 6.4, 6.9
                     , 5.5, 6.5, 5.7, 6.3, 4.9, 6.6, 5.2, 5., 5.9, 6., 6.1, 5.6, 6.7, 5.6, 5.8, 6.2, 5.6, 5.9
                     , 6.1, 6.3, 6.1, 6.4, 6.6, 6.8, 6.7, 6., 5.7, 5.5, 5.5, 5.8, 6., 5.4, 6., 6.7, 6.3, 5.6
                     , 5.5, 5.5, 6.1, 5.8, 5., 5.6, 5.7, 5.7, 6.2, 5.1, 5.7, 6.3, 5.8, 7.1, 6.3, 6.5, 7.6, 4.9
                     , 7.3, 6.7, 7.2, 6.5, 6.4, 6.8, 5.7, 5.8, 6.4, 6.5, 7.7, 7.7, 6., 6.9, 5.6, 7.7, 6.3, 6.7
                     , 7.2, 6.2, 6.1, 6.4, 7.2, 7.4, 7.9, 6.4, 6.3, 6.1, 7.7, 6.3, 6.4, 6., 6.9, 6.7, 6.9, 5.8
                     , 6.8, 6.7, 6.7, 6.3, 6.5, 6.2, 5.9])
    l = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     , 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
                     , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
                     , 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2
                     , 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2
                     , 2, 2, 2, 2, 2, 2, 2])
    return v, l
