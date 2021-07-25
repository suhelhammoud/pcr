import numpy as np

from pcr.item import ItemA
from pcr.instances_meta import AType


def none_missing(att, labels, att_type=AType.numeric, lines=None):
    """
    :param att: attribute values,
    :param labels: corresponding labels values
    :param att_type: numeric or nominal
    :param lines: only selected lines
    :return: non missing selected values of att and labels
    """
    if lines is not None:
        att = att[lines]
        labels = labels[lines]

    mask = att != -1 if att_type == AType.nominal else np.nan
    return att[mask], labels[mask]


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
    :return: (mx_rank_item,
            mx_rank_value,
            mx_lbl_index,
            mx_lbl_count)
    """
    if lbl_index is None:
        supp = np.amax(lbl_count, axis=1)
    else:
        supp = lbl_count[:, lbl_index]
    occ = np.sum(lbl_count, axis=1)
    rnk = supp / occ + 1 + supp / 1e6
    rnk = np.where(supp >= min_supp, rnk, float('-inf'))
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
    idx = att == item.itm_index \
        if item.a_type == AType.nominal \
        else np.logical_and(att >= item.lower, att < item.upper)
    return lines[idx]


def get_diff(all_lines, sub_lines):
    return np.setdiff1d(all_lines, sub_lines, assume_unique=True)
