import numpy as np

from item import identity_item
from instances import Instances, get_instances
from lines import count_labels_nominal, \
    get_max_item, get_covered_by_item, get_ranges
from rule import Rule
from instances_meta import AType


def best_rules(instances: Instances,
               min_supp: int,
               add_default_rule=False):
    rules = []
    lines_remained = np.arange(instances.num_instances(), dtype=np.int32)
    while len(lines_remained) >= min_supp:
        rule = best_rule(instances, min_supp, lines_remained)

        if rule is None:
            break

        lines_remained = np.setdiff1d(lines_remained,
                                      rule.lines,
                                      assume_unique=True)
        # rule clean lines
        rule.lines = None
        rules.append(rule)

    if add_default_rule:
        pass
    return rules


def best_rule(data: Instances,
              min_supp: int,
              lines: np.array):
    if lines.size < min_supp:
        return None

    available_atts = data.meta.att_indexes()
    num_lbl = data.meta.num_labels()
    # for the first time
    mx_item = identity_item
    for att_index in available_atts:
        tp = data.a_type(att_index)
        # tp = AType.numeric
        att = data.data[att_index][lines]
        lbl = data.labels[lines]
        if tp == AType.nominal:
            num_items = data.meta.num_items(att_index)
            lbl_count = count_labels_nominal(att,
                                             lbl,
                                             num_lbl,
                                             num_items)
        else:
            lbl_count, nitems = get_ranges(att, lbl, num_lbl)

        mx = get_max_item(lbl_count, min_supp)
        mx.att_index = att_index
        mx.a_type = tp

        if tp == AType.numeric:
            mx.lower = nitems[mx.index][0]
            mx.upper = nitems[mx.index][1]
            print('ok')

        mx_item = mx_item.max(mx)

    rule = Rule(mx_item.lbl_index)
    rule.add_test(mx_item)
    available_atts.remove(mx_item.att_index)
    att = data.data[mx_item.att_index]
    rule.lines = get_covered_by_item(att[lines], lines, mx_item)
    if rule.errors() == 0:
        return rule

    while rule.errors() > 0 and \
            len(available_atts) > 0 and \
            rule.correct() >= min_supp and \
            rule.lines.size > 0:
        mx_item = identity_item
        for att_index in available_atts:
            tp = data.a_type(att_index)
            att = data.atts(att_index)[lines]
            lbl = data.labels()[lines]
            if tp == AType.nominal:
                num_items = data.meta.num_items(att_index)
                lbl_count = count_labels_nominal(att,
                                                 lbl,
                                                 num_lbl,
                                                 num_items)
            else:
                lbl_count, nitems = get_ranges(att, lbl, num_lbl)

            mx = get_max_item(lbl_count, min_supp)
            mx_item = mx_item.max(mx)
        if mx_item.lbl_index == -1:
            break

        if not rule.can_enhance_rule(mx_item):
            break

        rule.add_test(mx_item)
        available_atts.remove(mx_item.att_index)
        att = data.atts(mx_item.att_index)

        rule.lines = get_covered_by_item(att[rule.lines], rule.lines, mx_item)
    assert rule.size() > 0
    return rule


if __name__ == '__main__':
    data = get_instances()
    num_items = data.meta.num_items()
    num_labels = num_items[-1]
    num_items = num_items[:-1]
    a_types = data.meta.a_type()
    all_lines = np.arange(0, data.num_instances(), dtype=np.int32)

    rules = best_rules(data, min_supp=2)
