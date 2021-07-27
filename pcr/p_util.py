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


def best_rule(instances: Instances,
              min_supp: int,
              lines: np.array):
    if lines.size < min_supp:
        return None

    available_atts = list(range(instances.num_attributes()))
    # for the first time
    mx_item = identity_item
    for att_index in available_atts:
        a_type = instances.a_type(att_index)
        att = instances.data[att_index][lines]  # TODO not needed for the first time
        labels = instances.labels[lines]
        if a_type == AType.nominal:
            lbl_count = count_labels_nominal(att,
                                             labels,
                                             instances.num_labels(),
                                             instances.num_items(att_index))
        else:
            lbl_count, ranges = get_ranges(att,
                                           labels,
                                           instances.num_labels())

        mx = get_max_item(lbl_count, min_supp)
        mx.att_index = att_index
        mx.a_type = a_type

        if a_type == AType.numeric:
            mx.lower = ranges[mx.index][0]
            mx.upper = ranges[mx.index][1]

        mx_item = mx_item.max(mx)

    rule = Rule(mx_item.lbl_index)
    rule.add_test(mx_item)
    available_atts.remove(mx_item.att_index)
    att = instances.data[mx_item.att_index]
    rule.lines = get_covered_by_item(att[lines], lines, mx_item)
    if rule.errors() == 0:
        return rule

    while rule.errors() > 0 and \
            len(available_atts) > 0 and \
            rule.correct() >= min_supp and \
            rule.lines.size > 0:
        mx_item = identity_item
        for att_index in available_atts:
            a_type = instances.a_type(att_index)
            att = instances.data[att_index][lines]
            labels = instances.labels[lines]
            if a_type == AType.nominal:
                lbl_count = count_labels_nominal(att,
                                                 labels,
                                                 instances.num_labels(),
                                                 instances.num_items(att_index))
            else:
                lbl_count, t_ranges = get_ranges(att,
                                                 labels,
                                                 instances.num_labels())

            mx = get_max_item(lbl_count, min_supp)
            mx.a_type = a_type

            if a_type == AType.numeric:
                mx.lower = t_ranges[mx.index][0]
                mx.upper = t_ranges[mx.index][1]

            mx_item = mx_item.max(mx)

        if mx_item.lbl_index == -1:
            break

        if not rule.can_enhance_rule(mx_item):
            break

        rule.add_test(mx_item)
        assert mx_item.att_index in available_atts
        available_atts.remove(mx_item.att_index)
        att = instances.atts(mx_item.att_index)

        rule.lines = get_covered_by_item(att[rule.lines], rule.lines, mx_item)
    assert rule.size() > 0
    return rule


if __name__ == '__main__':
    data: Instances = get_instances()

    print(data.num_attributes())
    print(data.num_instances())
    print(data.num_labels())
    print(data.num_items())
    print(data.a_type())

    rule = best_rule(data, 2, np.arange(data.num_instances()))

    print(rule.correct())