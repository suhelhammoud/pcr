import numpy as np

from item import ItemA
from instances_meta import AType
from instances import missing_nominal
from constants import missing_numeric, min_float


def none_missing(att,
                 lbl,
                 att_type=AType.numeric,
                 lines=None):
    """
    :param att: attribute values,
    :param lbl: corresponding labels values
    :param att_type: numeric or nominal
    :param lines: only selected lines
    :return: non missing selected values of att and labels
    """
    if lines is not None:
        att = att[lines]
        lbl = lbl[lines]

    if att_type == AType.nominal:
        mask = att != missing_nominal
    else:
        mask = att != missing_numeric
    return att[mask], lbl[mask]


def count_labels_nominal(
        att: np.array,
        labels: np.array,
        num_labels: int,
        num_items: int):
    temp = att * num_labels + labels
    return np.split(np.bincount(temp, minlength=num_labels * num_items),
                    num_items)


def count_labels(labels: np.array, num_lbl: int):
    return np.bincount(labels, minlength=num_lbl)


def get_max_item(lbl_count, min_supp, lbl_index=None):
    """

    :param lbl_count:
    :param min_supp:
    :param lbl_index:
    :return:
    """
    if lbl_index is None:
        supp = np.amax(lbl_count, axis=1)
    else:
        supp = lbl_count[:, lbl_index]
    occ = np.sum(lbl_count, axis=1)
    rnk = supp / occ + 1 + supp / 1e6
    rnk = np.where(supp >= min_supp, rnk, min_float)
    mx_rank_item = np.argmax(rnk)
    mx_rank_value = rnk[mx_rank_item]
    mx_lbl_count = lbl_count[mx_rank_item]
    mx_lbl_index = np.argmax(mx_lbl_count)
    return ItemA(-1,
                 mx_lbl_index,
                 mx_lbl_count,
                 mx_rank_value,
                 AType.nominal,
                 mx_rank_item)


def get_covered_by_item(att, lines, item: ItemA):
    idx = att == item.index \
        if item.a_type == AType.nominal \
        else np.logical_and(item.lower <= att, att < item.upper)
    return lines[idx]


def sliding_window(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def get_ranges(att: np.array,
               lbl: np.array,
               num_lbl):
    idx = np.argsort(att)
    att_sorted = att[idx]
    lbl_sorted = lbl[idx]

    a_dif = np.diff(att_sorted)
    lbl_dif = np.diff(lbl_sorted)

    splits = np.logical_or(a_dif == 0, lbl_dif == 0)
    result = np.where(splits is False)[0] + 1
    print(result)
    splt = np.split(att_sorted, result)
    ranges = np.array([[a[0], a[-1]] for a in splt])
    lbl_splt = np.split(lbl_sorted, result)
    counts = np.array([np.bincount(a, minlength=num_lbl) for a in lbl_splt])
    return counts, ranges
